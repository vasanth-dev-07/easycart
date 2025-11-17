# Development Setup Guide – EasyCart

This document explains how to set up and run the EasyCart project on your local development system. It is designed to help any new developer onboard quickly with a consistent setup process.

---

## 📌 Purpose of This File

* To guide new developers on how to run the project locally
* To ensure setup steps are standard for everyone
* To reduce confusion and save onboarding time

---

## 🧰 Requirements / Prerequisites

Make sure the following tools are installed:

* Python 3.10+
* Django 5+
* Git
* Virtual Environment (venv)
* SQLite (default) or PostgreSQL (optional)
* Node.js & npm (optional for frontend)

---

## 🚀 Clone the Repository

```bash
git clone git@github.com:vasanth-dev-07/easycart.git
cd easycart
```

---

## ⚙️ Backend Setup

### 1️⃣ Create Virtual Environment

```bash
python3 -m venv venv
```

### 2️⃣ Activate Virtual Environment

#### macOS / Linux

```bash
source venv/bin/activate
```

#### Windows (PowerShell)

```powershell
venv\Scripts\Activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create Environment File

```bash
cp .env.example .env
```

> Then update `.env` values such as `SECRET_KEY`, database credentials, and email configuration.

### 5️⃣ Apply Migrations

```bash
python manage.py migrate
```

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

The server runs at:

```
http://127.0.0.1:8000/
```

---

## 📂 Project Structure

```
easycart/
├── venv/                     # Virtual environment
├── backend/ or project/      # Main Django project directory
├── app/                      # Django apps
├── requirements.txt          # Python dependencies
├── manage.py                 # Django entrypoint
├── dev-setup.md              # This documentation file
└── README.md
```

---

## 🔧 Useful Commands

| Command                            | Description              |
| ---------------------------------- | ------------------------ |
| `pip freeze > requirements.txt`    | Update dependencies file |
| `python manage.py createsuperuser` | Create admin account     |
| `deactivate`                       | Exit virtual environment |

---

## 🤝 Contributing

### Create a new branch

```bash
git checkout -b feature-name
```

### Commit changes

```bash
git commit -m "Add feature"
```

### Push branch

```bash
git push origin feature-name
```

---

## 🧑‍💻 Author

**Vasanth Kumar** – Python Backend Developer | EasyCart Project




🛠️ Troubleshooting (Common Issues)

❗ Missing .env file or variables

Error: KeyError: 'SECRET_KEY' or email/db config errors
Fix:

cp .env.example .env


Fill required fields.

❗ Migration / DB errors

Error: no such table: or relation does not exist
Fix:

python manage.py migrate --run-syncdb

❗ Server Won’t Start

Try:

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

❗ Missing migrations
python manage.py makemigrations
python manage.py migrate


Always commit migration files inside each app’s migrations/ folder.
