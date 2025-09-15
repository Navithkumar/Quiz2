# Quiz2

# Employee Data Generation & Visualization System

A Django-based web application for generating synthetic employee data, storing it in PostgreSQL, and providing REST API endpoints with analytical summaries and visualizations.

## Features

-   **Synthetic Data Generation**: Create realistic employee records using Faker library
-   **RESTful API**: Comprehensive API endpoints with token authentication
-   **PostgreSQL Integration**: Persistent data storage with proper relationships
-   **Data Visualization**: Interactive charts using Chart.js
-   **API Documentation**: Swagger UI for interactive API exploration
-   **Authentication**: Token-based authentication for secure access
-   **Filtering & Pagination**: Advanced data retrieval options

## Technology Stack

-   **Backend**: Django 4.2.7, Django REST Framework 3.14.0
-   **Database**: PostgreSQL
-   **Authentication**: Token Authentication
-   **Documentation**: Swagger UI with drf-yasg
-   **Data Generation**: Faker library
-   **Visualization**: Chart.js

## Prerequisites

-   Python 3.8+
-   PostgreSQL 13+
-   pip (Python package manager)
-   Virtualenv (recommended)

## Quick Start

### Option 1: Local Development Setup

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd employee-data-system
    ```

2. **Create and activate virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up PostgreSQL database**

    ```bash
    # Create database in PostgreSQL
    createdb employee_db
    ```

5. **Configure environment variables**

    ```bash
    # Create .env file from example
    cp .env.example .env
    # Edit .env with your database credentials
    ```

6. **Run migrations**

    ```bash
    python manage.py migrate
    ```

7. **Generate sample data**

    ```bash
    python manage.py generate_sample_data
    ```

8. **Create superuser (optional)**

    ```bash
    python manage.py createsuperuser
    ```

9. **Run development server**

    ```bash
    python manage.py runserver
    ```

10. **Access the application**
    - API: http://localhost:8000/api/
    - Admin: http://localhost:8000/admin/
    - Swagger UI: http://localhost:8000/swagger/
    - Login Page: http://localhost:8000/api/auth/token/
      Add Token to Request Headers

10.1 **Setting Up Postman for Token Authentication**

-   Open Postman and create a new request

-   Set the request method to GET (or whatever method you need)

-   Enter your API endpoint URL: http://localhost:8000/api/employees/

-   Go to the Headers tab

-   Add a new header:

-   Key: Authorization

-   Value: Token e79233c9203f2e294ae66913aee8c4a5b8e66353 \*\*

### Option 2: Docker Setup

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd employee-data-system
    ```

2. **Build and start containers**

    ```bash
    docker-compose up --build
    ```

3. **Run migrations**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. **Generate sample data**

    ```bash
    docker-compose exec web python manage.py generate_sample_data
    ```

5. **Access the application**
    - API: http://localhost:8000/api/
    - Admin: http://localhost:8000/admin/
    - Swagger UI: http://localhost:8000/swagger/

## Default Credentials

After running the sample data generation, use these credentials:

-   **Admin User**:
    -   Username: `admin_1`
    -   Password: `admin123`
    -   Email: `admin@example.com`

## API Usage

### Authentication

1. **Get authentication token**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' http://localhost:8000/api/auth/token/
    ```

2. **Use token in API requests**
    ```bash
    curl -H "Authorization: Token YOUR_TOKEN_HERE" http://localhost:8000/api/employees/
    ```

### Available Endpoints

-   `GET /api/employees/` - List all employees
-   `GET /api/departments/` - List all departments
-   `GET /api/attendance/` - List attendance records
-   `GET /api/performance-reviews/` - List performance reviews
-   `GET /api/departments/analytics/` - Department analytics
-   `GET /api/attendance/analytics/` - Attendance analytics
-   `GET /api/dashboard/` - Dashboard statistics

# API Endpoints Documentation

## Base URL

All APIs are available at: `http://localhost:8000/api/`

## Authentication

### Obtain Authentication Token

-   **Endpoint**: `POST /api/auth/token/`
-   **Description**: Get authentication token for API access
-   **Request Body**:
    ```json
    {
        "username": "admin",
        "password": "admin123"
    }
    ```
-   **Response**:
    ```json
    {
        "token": "e79233c9203f2e294ae66913aee8c4a5b8e66353"
    }
    ```

## Employee Management

### List All Employees

-   **Endpoint**: `GET /api/employees/`
-   **Description**: Get paginated list of all employees
-   **Query Parameters**:
    -   `department` (optional): Filter by department name
    -   `employment_type` (optional): Filter by employment type (FT, PT, CT, IN)
    -   `page` (optional): Page number for pagination
-   **Response**:
    ```json
    {
        "count": 20,
        "next": "http://localhost:8000/api/employees/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "hire_date": "2023-05-15",
                "job_title": "Software Engineer",
                "salary": "75000.00",
                "department": 1,
                "department_name": "Engineering",
                "employment_type": "FT",
                "manager": null,
                "manager_name": null,
                "date_of_birth": "1990-05-15",
                "address": "123 Main St, Anytown, USA"
            }
        ]
    }
    ```

### Get Specific Employee

-   **Endpoint**: `GET /api/employees/{id}/`
-   **Description**: Get details of a specific employee
-   **Response**: Employee object

### Create Employee

-   **Endpoint**: `POST /api/employees/`
-   **Description**: Create a new employee
-   **Request Body**: Employee object fields
-   **Response**: Created employee object

### Update Employee

-   **Endpoint**: `PUT /api/employees/{id}/`
-   **Description**: Update an existing employee
-   **Request Body**: Employee object fields
-   **Response**: Updated employee object

### Delete Employee

-   **Endpoint**: `DELETE /api/employees/{id}/`
-   **Description**: Delete an employee
-   **Response**: 204 No Content

## Department Management

### List All Departments

-   **Endpoint**: `GET /api/departments/`
-   **Description**: Get list of all departments with employee counts
-   **Response**:
    ```json
    [
        {
            "id": 1,
            "name": "Engineering",
            "description": "Engineering Department",
            "location": "Floor 3",
            "budget": "500000.00",
            "established_date": "2020-01-15",
            "head_of_department": "Jane Smith",
            "email": "engineering@company.com",
            "employee_count": 8
        }
    ]
    ```

### Get Specific Department

-   **Endpoint**: `GET /api/departments/{id}/`
-   **Description**: Get details of a specific department
-   **Response**: Department object with employee count

### Create Department

-   **Endpoint**: `POST /api/departments/`
-   **Description**: Create a new department
-   **Request Body**: Department object fields
-   **Response**: Created department object

### Update Department

-   **Endpoint**: `PUT /api/departments/{id}/`
-   **Description**: Update an existing department
-   **Request Body**: Department object fields
-   **Response**: Updated department object

### Delete Department

-   **Endpoint**: `DELETE /api/departments/{id}/`
-   **Description**: Delete a department
-   **Response**: 204 No Content

## Attendance Management

### List All Attendance Records

-   **Endpoint**: `GET /api/attendance/`
-   **Description**: Get paginated list of all attendance records
-   **Query Parameters**:
    -   `employee` (optional): Filter by employee name
    -   `date` (optional): Filter by specific date
    -   `status` (optional): Filter by status (PR, AB, LV, HD, LT)
    -   `page` (optional): Page number for pagination
-   **Response**: Paginated list of attendance records

### Get Specific Attendance Record

-   **Endpoint**: `GET /api/attendance/{id}/`
-   **Description**: Get details of a specific attendance record
-   **Response**: Attendance object

### Create Attendance Record

-   **Endpoint**: `POST /api/attendance/`
-   **Description**: Create a new attendance record
-   **Request Body**: Attendance object fields
-   **Response**: Created attendance object

### Update Attendance Record

-   **Endpoint**: `PUT /api/attendance/{id}/`
-   **Description**: Update an existing attendance record
-   **Request Body**: Attendance object fields
-   **Response**: Updated attendance object

### Delete Attendance Record

-   **Endpoint**: `DELETE /api/attendance/{id}/`
-   **Description**: Delete an attendance record
-   **Response**: 204 No Content

## Performance Reviews

### List All Performance Reviews

-   **Endpoint**: `GET /api/performance-reviews/`
-   **Description**: Get paginated list of all performance reviews
-   **Query Parameters**:
    -   `employee` (optional): Filter by employee name
    -   `min_rating` (optional): Filter by minimum rating (1-5)
    -   `page` (optional): Page number for pagination
-   **Response**: Paginated list of performance reviews

### Get Specific Performance Review

-   **Endpoint**: `GET /api/performance-reviews/{id}/`
-   **Description**: Get details of a specific performance review
-   **Response**: Performance review object

### Create Performance Review

-   **Endpoint**: `POST /api/performance-reviews/`
-   **Description**: Create a new performance review
-   **Request Body**: Performance review object fields
-   **Response**: Created performance review object

### Update Performance Review

-   **Endpoint**: `PUT /api/performance-reviews/{id}/`
-   **Description**: Update an existing performance review
-   **Request Body**: Performance review object fields
-   **Response**: Updated performance review object

### Delete Performance Review

-   **Endpoint**: `DELETE /api/performance-reviews/{id}/`
-   **Description**: Delete a performance review
-   **Response**: 204 No Content

## Analytics Endpoints

### Department Analytics

-   **Endpoint**: `GET /api/departments/analytics/`
-   **Description**: Get analytical data for all departments
-   **Response**:
    ```json
    [
        {
            "department": "Engineering",
            "employee_count": 8,
            "avg_salary": "78500.00",
            "total_budget": "500000.00",
            "budget_utilization": 62.8
        }
    ]
    ```

### Attendance Analytics

-   **Endpoint**: `GET /api/attendance/analytics/`
-   **Description**: Get analytical data for attendance over the last 30 days
-   **Response**:
    ```json
    [
        {
            "date": "2024-01-15",
            "present_count": 18,
            "absent_count": 2,
            "late_count": 3,
            "attendance_rate": 90.0
        }
    ]
    ```

### Employee Dashboard

-   **Endpoint**: `GET /api/dashboard/`
-   **Description**: Get dashboard statistics and recent hires
-   **Response**:
    ```json
    {
        "total_employees": 20,
        "total_departments": 5,
        "today_attendance": 18,
        "recent_hires": [
            {
                "id": 19,
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.j@example.com",
                "hire_date": "2024-01-10",
                "job_title": "Marketing Specialist",
                "department_name": "Marketing"
            }
        ]
    }
    ```

## Web Interface Endpoints

### Login Page

-   **Endpoint**: `GET /api/login/`
-   **Description**: HTML login page for token-based authentication
-   **Response**: HTML page with login form

### Dashboard View

-   **Endpoint**: `GET /api/dashboard/view/`
-   **Description**: HTML dashboard with data visualizations
-   **Response**: HTML page with charts and analytics

## Authentication Requirements

All API endpoints (except the token authentication endpoint) require authentication using the token in the request header:

```
Authorization: Token e79233c9203f2e294ae66913aee8c4a5b8e66353
```

## Rate Limiting

The API implements rate limiting:

-   Anonymous users: 100 requests per day
-   Authenticated users: 1000 requests per day

## Error Responses

Common error responses:

### 400 Bad Request

```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized

```json
{
    "detail": "Invalid token."
}
```

### 403 Forbidden

```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
    "detail": "Not found."
}
```

### 429 Too Many Requests

```json
{
    "detail": "Request was throttled."
}
```


## API Documentation

Interactive API documentation is available at:

-   Swagger UI: `http://localhost:8000/swagger/`
-   ReDoc: `http://localhost:8000/redoc/`

The documentation includes detailed information about each endpoint, request/response schemas, and allows you to test the API directly from the browser.

### Filtering Examples

-   Filter employees by department: `/api/employees/?department=Engineering`
-   Filter attendance by date: `/api/attendance/?date=2024-01-15`
-   Filter performance reviews by rating: `/api/performance-reviews/?min_rating=4`

## Data Models

The application includes four main models:

1. **Department**: Organizational departments with budget information
2. **Employee**: Employee details with department relationships
3. **Attendance**: Daily attendance records for employees
4. **PerformanceReview**: Performance evaluation records

## Customization

### Generating More Sample Data

Edit `employees/management/commands/generate_sample_data.py` to modify:

-   Number of employees generated
-   Date ranges for records
-   Salary ranges and distributions
-   Department configurations

### Adding New Fields

1. Add field to appropriate model in `models.py`
2. Create and run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update serializer in `serializers.py`
4. Update data generation command if needed

## API Documentation

Interactive API documentation is available at `/swagger/` and `/redoc/` endpoints. The documentation includes:

-   All available endpoints
-   Request/response schemas
-   Authentication requirements
-   Interactive testing capability

## Troubleshooting

### Common Issues

1. **Database connection errors**

    - Verify PostgreSQL is running
    - Check database credentials in `.env` file

2. **Authentication failures**

    - Ensure you've run `generate_sample_data` to create the admin user
    - Verify token is correctly formatted: `Token YOUR_TOKEN_HERE`

3. **Missing dependencies**

    - Run `pip install -r requirements.txt` to ensure all packages are installed

4. **CORS issues**
    - Check `CORS_ALLOW_ALL_ORIGINS` setting in `config/settings.py`

### Getting Help

If you encounter issues:

1. Check the Django server logs for error messages
2. Verify all migration steps were completed
3. Ensure the sample data generation ran successfully

## Development

### Project Structure

```
employee-data-system/
├── config/                 # Django project settings
├── employees/             # Main application
│   ├── management/        # Custom management commands
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   └── urls.py           # Application URLs
├── .env                   # Environment variables
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Docker image definition
└── requirements.txt      # Python dependencies
```

### Adding New Features

1. Create model in `models.py`
2. Generate and run migrations
3. Create serializer in `serializers.py`
4. Implement views in `views.py`
5. Add URL patterns in `urls.py`
6. Update API documentation if needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

-   Built with Django and Django REST Framework
-   Uses Faker for synthetic data generation
-   Chart.js for data visualization
-   PostgreSQL for data persistence

## Potential Improvements

-   **Refactor Folder Structure**  
    Organize the project into a cleaner, scalable structure (similar to the reference layout) for easier maintenance and feature growth.

-   **Performance Enhancements**  
    Set up **Redis caching** and **RabbitMQ** to handle background tasks, improve scalability, and reduce response latency.

-   **Custom API Responses**  
    Standardize API responses with a consistent format (status, message, data, error codes) to improve client-side handling and debugging.

-   **Custom Pagination**  
    Implement tailored pagination (limit-offset, cursor-based, or page-based) with a uniform schema in API responses for better data consumption.
