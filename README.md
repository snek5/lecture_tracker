# Seminar Tracker

A modern, responsive web application for tracking seminars and talks. Built with Flask, Bootstrap 5, and HTMX for a seamless user experience.

## Features

- **User Authentication**: Secure registration and login with Flask-Login
- **Dashboard**: Overview of your seminars with metrics (total count, hours, averages)
- **Seminar Management**: Create, edit, and delete seminars
- **Search & Sort**: Full-text search and dynamic sorting by date, topic, speaker, hours, or organizer
- **Inline Editing**: Edit seminar details directly in the dashboard table with inline forms
- **Delete Confirmation**: Confirmation modal before deleting seminars
- **Excel Export**: Export your seminars to an Excel spreadsheet
- **Responsive Design**: Built with Bootstrap 5 for a mobile-friendly interface
- **User Isolation**: Each user's seminars are securely isolated—users can only see their own data
- **Real-time Updates**: HTMX-powered modals and partial page updates without full page reloads

## Tech Stack

- **Backend**: Flask 3.0.3 with Flask-SQLAlchemy ORM
- **Authentication**: Flask-Login with secure session management
- **Frontend**: Bootstrap 5.3.3 + HTMX 1.9+ for dynamic interactions
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Forms**: Flask-WTF with automatic CSRF protection and validation
- **Export**: openpyxl for Excel generation
- **Testing**: pytest with comprehensive test coverage

## Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd seminar
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask app:
```bash
flask --app wsgi run
```

The app will be available at `http://127.0.0.1:5000`

### Default Test User

Username: `test`  
Password: `12345678`

## Project Structure

```
.
├── app/
│   ├── __init__.py           # App factory and blueprint registration
│   ├── config.py             # Configuration classes (dev, prod, test)
│   ├── models.py             # SQLAlchemy models (User, Seminar)
│   ├── forms.py              # Flask-WTF form definitions
│   ├── extensions.py         # Flask extensions (db, login_manager, etc.)
│   ├── routes/
│   │   ├── auth.py           # Login, register, logout routes
│   │   ├── dashboard.py      # Dashboard with search/sort
│   │   └── seminar.py        # CRUD operations for seminars
│   ├── templates/
│   │   ├── base.html         # Base template with navbar and auth
│   │   ├── dashboard.html    # Dashboard page with table
│   │   ├── auth/
│   │   │   ├── register.html
│   │   │   └── login.html
│   │   └── partials/
│   │       ├── seminar_modal.html
│   │       ├── seminar_form.html
│   │       ├── seminar_inline_form.html
│   │       └── seminar_inline_view.html
│   └── static/
│       └── css/style.css     # Custom theming (maroon/yellow/grey palette)
├── tests/
│   └── test_app.py           # Comprehensive test suite (10+ tests)
├── wsgi.py                   # WSGI entry point for deployment
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata and build config
├── Dockerfile                # Docker container configuration
├── .dockerignore              # Files excluded from Docker build
├── .gitignore                # Git ignore rules
└── pytest.ini                # pytest configuration
```

## Usage

### Adding a Seminar

1. Log in to your account
2. Click "Add New Seminar" on the dashboard
3. Fill in the seminar details (date, topic, speaker, hours, organizer, notes)
4. Click "Save Seminar"
5. The new seminar appears in your dashboard

### Searching & Sorting

- **Search**: Use the search box to find seminars by topic, speaker, organizer, or notes
- **Sort**: Click on column headers or use the sort dropdown to reorder seminars
- **Direction**: Toggle between ascending and descending order

### Editing & Deleting

- **Inline Edit**: Click the "Edit" button next to a seminar to edit it in-place
- **Delete**: Click the "Delete" button, confirm in the modal, and the seminar is removed

### Exporting

Click "Export to Excel" to download all your seminars as an Excel spreadsheet.

## Testing

Run the test suite to verify all functionality:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app tests/
```

## Docker Deployment

Build and run the app in a Docker container:

```bash
# Build the image
docker build -t seminar-tracker .

# Run the container
docker run -p 5000:5000 seminar-tracker
```

For production, set environment variables:

```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  seminar-tracker
```

## Configuration

Configuration is managed via environment variables. See `app/config.py` for available options:

- `FLASK_ENV`: Set to `production` for production deployments
- `SECRET_KEY`: Secret key for session encryption (required for production)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `DEBUG`: Enable/disable debug mode

## Security Notes

- User passwords are hashed using Werkzeug security utilities
- All forms include CSRF protection via Flask-WTF
- Database queries use SQLAlchemy parameterized queries to prevent SQL injection
- User data is isolated—each user can only access their own seminars
- Sessions are secure and HTTP-only

## Color Scheme

- **Primary**: Maroon (#6f1d2d) - Used for primary actions and emphasis
- **Secondary**: Yellow (#ebc85d) - Used for secondary actions and accents
- **Neutral**: Light Grey (#f3f4f6) - Used for backgrounds and neutral UI elements

## Future Enhancements

- [ ] Pagination for large seminar lists
- [ ] Tag-based filtering
- [ ] Seminar categories
- [ ] Import from CSV
- [ ] Email reminders for upcoming seminars
- [ ] Calendar view of seminars
- [ ] Statistics and analytics dashboard

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please follow the existing code style and add tests for new features.

## Support

For issues or feature requests, please open an issue on the repository.
