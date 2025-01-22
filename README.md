# Django Boilerplate

A simple and evolving boilerplate for Django projects, designed for fast and efficient development. This project includes basic configurations and tools to streamline my workflow.

---

## Features
- **Environment Variable Management**: Powered by `python-dotenv`.
- **PostgreSQL Integration**: Ready-to-use configuration for PostgreSQL databases.
- **Utility Scripts**: Includes a script to generate `.env.example` for easy setup.
- **Virtual Environment Support**: Follow best practices with isolated dependencies.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/django-boilerplate.git
cd django-boilerplate
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment
```bash
python -m venv ../venv
../venv/Scripts/activate.ps1  # Windows PowerShell
```
For macOS/Linux or Bash on Windows:

```bash
source ../venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Manually copy `.env.example` to `.env` and populate it with your environment-specific variables:
```env
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=True
```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

---

## Usage

### Generating an `.env.example`
To create or update the `.env.example` file:
```bash
python ../tools/generate_env_example.py
```

### Activating the Virtual Environment
```bash
../venv/Scripts/activate.ps1  # For Windows PowerShell
source ../venv/bin/activate   # For macOS/Linux
```

---

## Project Structure
```bash
zeeshan-shafeek-django-boiler-plate/
├── README.md
├── LICENSE
├── django_boilerplate/      # Main Django project files
│   ├── manage.py            # Django entry point
│   ├── requirements.txt
│   ├── .env.example         # Example environment variables
│   ├── apps/
│   │   ├── users/           # Custom user management app
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── tests.py
│   │   │   ├── views.py
│   │   │   └── migrations/
│   │   │       └── __init__.py
│   │   └── utils/           # Shared utilities
│   │       └── models.py    # BaseModel, Activable, Auditable
│   ├── django_boilerplate/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
├── tools/                   # Utility scripts
│   └── generate_env_example.py
├── venv/                    # Virtual environment (ignored by Git)
├── .gitignore
├── LICENSE
├── README.md
```

---

## Contributing
This boilerplate is primarily for personal use but is open to contributions. Feel free to fork the repository, submit pull requests, or suggest improvements.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
