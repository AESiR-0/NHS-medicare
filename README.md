# Medicare - NHS Staffing Management System

A Django-based web application for managing NHS staffing, connecting hospitals with nursing agencies.

## Features

- Three user roles: Admin, Agency, and Hospital
- NHS Trusts and Hospitals management
- Agency approval system for Trusts
- Nurse management with document upload
- Shift creation and booking system
- Role-based dashboards
- Modern UI with Tailwind CSS

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd medicare
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Seed initial data:
```bash
python manage.py seed_data
```

7. Run the development server:
```bash
python manage.py runserver
```

## Default Users

After running the seed_data command, the following users will be created:

### Admin
- Username: admin
- Password: admin123
- Email: admin@example.com

### Hospitals
1. St. Thomas Hospital
   - Username: hospital1
   - Password: hospital123
   - Email: hospital1@example.com

2. Manchester Royal Infirmary
   - Username: hospital2
   - Password: hospital123
   - Email: hospital2@example.com

### Agencies
1. London Nursing Agency
   - Username: agency1
   - Password: agency123
   - Email: agency1@example.com

2. Manchester Nursing Agency
   - Username: agency2
   - Password: agency123
   - Email: agency2@example.com

## Usage

1. Access the application at http://localhost:8000
2. Log in with one of the default users
3. Navigate through the role-specific dashboard
4. Use the admin interface at http://localhost:8000/admin for administrative tasks

## Project Structure

```
medicare/
├── core/                    # Main application
│   ├── management/         # Management commands
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── admin.py           # Admin interface configuration
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   └── urls.py            # URL routing
├── medicare/              # Project settings
├── static/                # Static files
├── media/                 # User-uploaded files
├── templates/             # Base templates
└── manage.py             # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 