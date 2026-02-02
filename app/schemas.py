from pydantic import BaseModel, EmailStr, field_validator
from datetime import date

class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str
    
    @field_validator('employee_id')
    @classmethod
    def validate_employee_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Employee ID cannot be empty')
        return v.strip()
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Full name cannot be empty')
        return v.strip()
    
    @field_validator('department')
    @classmethod
    def validate_department(cls, v):
        if not v or not v.strip():
            raise ValueError('Department cannot be empty')
        return v.strip()

class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    status: str
    
    @field_validator('employee_id')
    @classmethod
    def validate_employee_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Employee ID cannot be empty')
        return v.strip()
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in ['present', 'absent']:
            raise ValueError('Status must be either "present" or "absent"')
        return v
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v > date.today():
            raise ValueError('Cannot mark attendance for future dates')
        return v