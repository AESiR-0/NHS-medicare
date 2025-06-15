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

## Seed Data (for Testing)
After running the seed command, you can use these credentials to log in:

**Admin User:**
- Username: `seed_admin`
- Password: `admin123`

**Hospital User:**
- Username: `seed_hospital`
- Password: `hospital123`

**Agency User:**
- Username: `seed_agency`
- Password: `agency123`

## How to Use

### 1. Setup
- Clone the repository
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Run migrations:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- (Optional) Create a superuser:
  ```bash
  python manage.py createsuperuser
  ```
- Seed the database with test data:
  ```bash
  python manage.py seed_data
  ```
- Start the development server:
  ```bash
  python manage.py runserver
  ```

### 2. Access the Platform
- Visit [http://localhost:8000/admin](http://localhost:8000/admin) for the Django admin interface.
- Use the seed credentials above to log in as different roles.
- Explore the main app at [http://localhost:8000/](http://localhost:8000/)

### 3. Testing the Product
- Log in as **Admin** to manage users, approve agencies, and oversee the system.
- Log in as **Hospital** to create and manage shifts.
- Log in as **Agency** to view available shifts, book nurses, and upload nurse documents.
- Use the admin interface to view and manage all data.
- Test document expiry notifications by running:
  ```bash
  python manage.py check_expiring_documents --days 30
  ```

## Workflow Explanation

1. **Admin** creates and approves NHS Trusts, Agencies, and oversees the platform.
2. **NHS Trusts** can be linked to multiple Agencies via TrustAgencyAccess (with approval).
3. **Hospitals** (under a Trust) post available shifts specifying ward, specialty, and timing.
4. **Agencies** manage their nurses, upload/verify documents, and book nurses for open shifts.
5. **Nurses** are approved by agencies and must have valid documents to be booked for shifts.
6. **Shift Booking:**
   - Agencies view and book available shifts for their nurses.
   - Bookings can be confirmed or cancelled, with audit trails.
7. **Document Management:**
   - Agencies upload nurse documents (e.g., registration, ID, DBS).
   - Documents are verified and tracked for expiry.
   - Expiry notifications are sent to agencies.
8. **Dashboards** for each role provide relevant overviews and actions.

## Tech Stack & Architecture (for Presentation)

- **Backend:** Django 5.x (Python 3.11+)
- **Frontend:** Django Templates (HTML5, Tailwind CSS for styling)
- **Database:** SQLite (default, easy to switch to PostgreSQL/MySQL)
- **Authentication:** Custom User Model with role-based access (Admin, Agency, Hospital)
- **File Storage:** Local file storage for nurse documents
- **Email:** Django email backend for notifications (configurable)
- **Management Commands:**
  - `seed_data` for test data
  - `check_expiring_documents` for document expiry notifications
- **Testing:** Manual via admin and UI, extensible for automated tests

### Key Features
- Role-based dashboards and permissions
- Shift management and booking workflow
- Nurse document upload, verification, and expiry tracking
- Agency-Trust approval system
- Audit trails for approvals, bookings, and document actions
- Extensible for real-world NHS/healthcare staffing needs

## Demo & Presentation Tips
- Show login as each role and their dashboard
- Demonstrate shift creation, booking, and nurse document upload
- Run the expiry notification command to show email alerts
- Highlight the clean, modern UI and clear workflow
- Discuss how the architecture supports NHS/healthcare staffing at scale 