# HRMS Backend

A robust RESTful API built with FastAPI for managing employee records and attendance tracking.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic v2
- **CORS**: FastAPI CORS Middleware
- **Python**: 3.8+

## Database Schema

### Employees Table
```sql
create table public.employees (
  id uuid not null default gen_random_uuid (),
  employee_id text not null,
  full_name text not null,
  email text not null,
  department text not null,
  created_at timestamp without time zone null default now(),
  constraint employees_pkey primary key (id),
  constraint employees_email_key unique (email),
  constraint employees_employee_id_key unique (employee_id)
);
```

### Attendance Table
```sql
create table public.attendance (
  id uuid not null default gen_random_uuid (),
  employee_id uuid null,
  date date not null,
  status text not null,
  created_at timestamp without time zone null default now(),
  constraint attendance_pkey primary key (id),
  constraint attendance_employee_id_date_key unique (employee_id, date),
  constraint attendance_employee_id_fkey
    foreign key (employee_id)
    references employees (id)
    on delete cascade,
  constraint attendance_status_check
    check (status in ('present','absent','leave'))
);
```

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database (Supabase account recommended)
- pip (Python package manager)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/KunalRaj9835/HRMS-Backend.git
cd HRMS-B
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

**To get your Supabase DATABASE_URL:**
1. Go to your Supabase project dashboard
2. Navigate to Settings → Database
3. Find the "Connection string" section
4. Copy the URI format connection string
5. Replace `[YOUR-PASSWORD]` with your actual database password

### 5. Set Up Database Tables

Run the SQL schema in your Supabase SQL Editor or PostgreSQL client to create the required tables.

### 6. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | Get all employees |
| GET | `/employees/{employee_id}` | Get employee by ID |
| POST | `/employees` | Create new employee |
| PUT | `/employees/{employee_id}` | Update employee |
| DELETE | `/employees/{employee_id}` | Delete employee |

### Attendance

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/attendance` | Mark attendance |
| GET | `/attendance/{employee_id}` | Get attendance records |
| GET | `/attendance/{employee_id}?date=YYYY-MM-DD` | Get attendance for specific date |

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Request/Response Examples

### Create Employee
```bash
POST /employees
Content-Type: application/json

{
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "department": "Engineering"
}
```

### Mark Attendance
```bash
POST /attendance
Content-Type: application/json

{
  "employee_id": "EMP001",
  "date": "2024-02-02",
  "status": "present"
}
```

## Project Structure

```
HRMS-B/
├── app/
│   ├── __init__.py
│   ├── attendance.py      # Attendance routes and logic
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   ├── employees.py       # Employee routes and logic
│   └── schemas.py         # Pydantic models
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
└── README.md             # This file
```

## Dependencies

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.9
pydantic>=2.0.0
python-dotenv>=1.0.0
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |

## Assumptions & Limitations

### Assumptions
1. **Unique Employee IDs**: Each employee has a unique `employee_id` (e.g., EMP001)
2. **One Attendance Per Day**: An employee can only have one attendance record per day
3. **Valid Status Values**: Attendance status must be one of: `present`, `absent`, `leave`
4. **Date Format**: All dates use ISO 8601 format (YYYY-MM-DD)
5. **Employee Exists**: Attendance can only be marked for existing employees

### Limitations
1. **No Authentication**: Currently no user authentication or authorization implemented
2. **No Bulk Operations**: No endpoints for bulk employee creation or attendance marking
3. **Limited Reporting**: No built-in analytics or reporting features
4. **No File Upload**: Employee profile pictures or document uploads not supported
5. **Basic Validation**: Minimal business logic validation (e.g., can mark future attendance)
6. **No Caching**: No caching layer implemented for frequently accessed data
7. **No Rate Limiting**: API endpoints are not rate-limited
8. **Cascade Delete**: Deleting an employee removes all their attendance records

## Future Enhancements

- Add JWT-based authentication
- Implement role-based access control (Admin, Manager, Employee)
- Add bulk import/export functionality
- Generate attendance reports and analytics
- Add email notifications
- Implement attendance approval workflow
- Add support for shift timings and overtime
- WebSocket support for real-time updates

## Troubleshooting

### Database Connection Issues
```bash
# Verify your DATABASE_URL is correct
python -c "from app.database import engine; print(engine.url)"
```

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue in the GitHub repository.