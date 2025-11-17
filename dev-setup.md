# Development Setup Guide – EasyCart

This document explains how to set up and run the EasyCart project on your local development system. It is designed to help any new developer onboard quickly with a consistent setup process.

---

## 📌 Purpose of This File
- To guide new developers on how to run the project locally
- To ensure setup steps are standard for everyone
- To reduce confusion and save onboarding time

---

## 🧰 Requirements / Prerequisites
Make sure the following tools are installed:

- Python 3.10+
- Django 5+
- Git
- Virtual Environment (venv)
- SQLite (default) or PostgreSQL (optional)
- Node.js & npm (optional for frontend)

---

## 🚀 Clone the Repository
```bash
git clone git@github.com:vasanth-dev-07/easycart.git
cd easycart

2️⃣ Create Virtual Environment
python3 -m venv venv

3️⃣ Activate Virtual Environment
macOS / Linux
source venv/bin/activate

Windows
venv\Scripts\activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Apply Migrations
python manage.py migrate

6️⃣ Run Development Server
python manage.py runserver


Server will run at:

http://127.0.0.1:8000/

📂 Project Structure
easycart/
├── venv/                     # Virtual environment
├── backend/ or project/      # Main Django project directory
├── app/                      # Django apps
├── requirements.txt          # Python dependencies
├── manage.py                 # Django entrypoint
├── dev-setup.md              # This documentation file
└── README.md

🔧 Useful Commands

Command	Description

pip freeze > requirements.txt	Update dependencies file
python manage.py createsuperuser	Create admin account
deactivate	Exit virtual environment


🎯 Purpose of This File

Helps new developers quickly set up environment

Documents tools and versions used in development

Prevents onboarding confusion and setup errors

🤝 Contributing

Create a new branch for each feature

git checkout -b feature-name


Commit your changes

git commit -m "Add feature"


Push branch

git push origin feature-name

🧑‍💻 Author

Vasanth Kumar – Python Backend Developer | EasyCart Project