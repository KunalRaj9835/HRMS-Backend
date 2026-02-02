from fastapi import APIRouter, HTTPException
from app.database import supabase
from app.schemas import EmployeeCreate
from postgrest.exceptions import APIError

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("", status_code=201)
def add_employee(data: EmployeeCreate):
    """Add a new employee"""
    try:
        response = supabase.table("employees").insert(data.dict()).execute()
        return {"message": "Employee added successfully", "data": response.data}
    except APIError as e:
        # Handle duplicate key violations
        error_message = str(e.message) if hasattr(e, 'message') else str(e)
        
        if "employees_employee_id_key" in error_message:
            raise HTTPException(
                status_code=409,
                detail=f"Employee ID '{data.employee_id}' already exists"
            )
        elif "employees_email_key" in error_message:
            raise HTTPException(
                status_code=409,
                detail=f"Email '{data.email}' already exists"
            )
        else:
            raise HTTPException(
                status_code=409,
                detail=f"Conflict: {error_message}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("")
def list_employees():
    """List all employees"""
    try:
        response = supabase.table("employees").select("*").order("created_at", desc=True).execute()
        return {"employees": response.data, "count": len(response.data)}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching employees: {str(e)}"
        )

@router.get("/{employee_id}")
def get_employee(employee_id: str):
    """Get a specific employee by employee_id"""
    try:
        response = supabase.table("employees").select("*").eq("employee_id", employee_id).single().execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching employee: {str(e)}"
        )

@router.delete("/{employee_uuid}")
def delete_employee(employee_uuid: str):
    """Delete an employee by UUID"""
    try:
        response = supabase.table("employees").delete().eq("id", employee_uuid).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Employee not found")

        return {"message": "Employee deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting employee: {str(e)}"
        )