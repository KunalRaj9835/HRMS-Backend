from fastapi import APIRouter, HTTPException
from app.database import supabase
from app.schemas import AttendanceCreate
from postgrest.exceptions import APIError
from datetime import date as date_type

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("", status_code=201)
def mark_attendance(data: AttendanceCreate):
    """Mark attendance for an employee"""
    try:
        # Find employee by employee_id
        emp_response = supabase.table("employees").select("id").eq(
            "employee_id", data.employee_id
        ).execute()

        if not emp_response.data or len(emp_response.data) == 0:
            raise HTTPException(status_code=404, detail="Employee not found")

        employee_uuid = emp_response.data[0]["id"]

        payload = {
            "employee_id": employee_uuid,
            "date": data.date.isoformat(),
            "status": data.status
        }

        response = supabase.table("attendance").insert(payload).execute()
        return {"message": "Attendance marked successfully", "data": response.data}
        
    except HTTPException:
        raise
    except APIError as e:
        error_message = str(e.message) if hasattr(e, 'message') else str(e)
        
        if "attendance_employee_id_date_key" in error_message:
            raise HTTPException(
                status_code=409,
                detail=f"Attendance already marked for employee '{data.employee_id}' on {data.date}"
            )
        else:
            raise HTTPException(
                status_code=409,
                detail=f"Conflict: {error_message}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error marking attendance: {str(e)}"
        )

@router.get("/{employee_id}")
def get_attendance(employee_id: str, date: str | None = None):
    """Get attendance records for an employee"""
    try:
        # Find employee by employee_id
        emp_response = supabase.table("employees").select("id, employee_id, full_name").eq(
            "employee_id", employee_id
        ).execute()

        if not emp_response.data or len(emp_response.data) == 0:
            raise HTTPException(status_code=404, detail="Employee not found")

        employee_uuid = emp_response.data[0]["id"]
        employee_info = emp_response.data[0]

        # Build query
        query = supabase.table("attendance").select("*").eq("employee_id", employee_uuid)

        if date:
            query = query.eq("date", date)

        attendance_response = query.order("date", desc=True).execute()

        return {
            "employee": employee_info,
            "attendance": attendance_response.data,
            "count": len(attendance_response.data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching attendance: {str(e)}"
        )

@router.get("")
def list_all_attendance(date: str | None = None):
    """List all attendance records, optionally filtered by date"""
    try:
        query = supabase.table("attendance").select(
            "*, employees(employee_id, full_name, department)"
        )
        
        if date:
            query = query.eq("date", date)
        
        response = query.order("date", desc=True).execute()
        
        return {
            "attendance": response.data,
            "count": len(response.data)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching attendance records: {str(e)}"
        )

@router.get("/dashboard/summary")
def get_dashboard_summary(date: str | None = None):
    """Get dashboard summary statistics"""
    try:
        # Get total employees
        employees_response = supabase.table("employees").select("id", count="exact").execute()
        total_employees = employees_response.count or 0

        # If date is provided, get stats for that date
        if date:
            attendance_query = supabase.table("attendance").select(
                "*, employees(employee_id, full_name, department)"
            ).eq("date", date)
            
            attendance_response = attendance_query.execute()
            attendance_records = attendance_response.data
            
            present_count = sum(1 for record in attendance_records if record["status"] == "present")
            absent_count = sum(1 for record in attendance_records if record["status"] == "absent")
            leave_count = sum(1 for record in attendance_records if record["status"] == "leave")
            
            return {
                "total_employees": total_employees,
                "date": date,
                "present": present_count,
                "absent": absent_count,
                "leave": leave_count,
                "not_marked": total_employees - len(attendance_records),
                "attendance_records": attendance_records
            }
        else:
            # Get today's stats
            from datetime import datetime
            today = datetime.now().date().isoformat()
            
            attendance_query = supabase.table("attendance").select(
                "*, employees(employee_id, full_name, department)"
            ).eq("date", today)
            
            attendance_response = attendance_query.execute()
            attendance_records = attendance_response.data
            
            present_count = sum(1 for record in attendance_records if record["status"] == "present")
            absent_count = sum(1 for record in attendance_records if record["status"] == "absent")
            leave_count = sum(1 for record in attendance_records if record["status"] == "leave")
            
            return {
                "total_employees": total_employees,
                "date": today,
                "present": present_count,
                "absent": absent_count,
                "leave": leave_count,
                "not_marked": total_employees - len(attendance_records),
                "attendance_records": attendance_records
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching dashboard summary: {str(e)}"
        )

@router.get("/dashboard/stats")
def get_dashboard_stats(start_date: str | None = None, end_date: str | None = None):
    """Get attendance statistics for a date range (for charts)"""
    try:
        from datetime import datetime, timedelta
        
        # Default to last 7 days if no dates provided
        if not end_date:
            end_date = datetime.now().date().isoformat()
        if not start_date:
            start = datetime.fromisoformat(end_date) - timedelta(days=6)
            start_date = start.date().isoformat()
        
        # Get attendance records for the date range
        query = supabase.table("attendance").select(
            "date, status"
        ).gte("date", start_date).lte("date", end_date)
        
        response = query.execute()
        records = response.data
        
        # Group by date
        stats_by_date = {}
        current = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
        
        # Initialize all dates in range
        while current <= end:
            date_str = current.isoformat()
            stats_by_date[date_str] = {
                "date": date_str,
                "present": 0,
                "absent": 0,
                "leave": 0
            }
            current += timedelta(days=1)
        
        # Count records
        for record in records:
            date_str = record["date"]
            if date_str in stats_by_date:
                status = record["status"]
                if status in stats_by_date[date_str]:
                    stats_by_date[date_str][status] += 1
        
        # Convert to list sorted by date
        stats_list = sorted(stats_by_date.values(), key=lambda x: x["date"])
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "daily_stats": stats_list
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching dashboard stats: {str(e)}"
        )