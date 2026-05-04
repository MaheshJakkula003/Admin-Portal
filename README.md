# Qatar Foundation — Admin Portal

This project is a complete backend implementation for the CertifyMe Admin Portal intern task. Built with Flask and SQLite, it supports full user authentication and a CRUD system for managing opportunities.

## Features
- **Authentication:** Secure Admin Sign Up, Login (with "Remember Me" session persistence), and Forgot Password (with secure, 1‑hour expiring tokens).
- **Opportunity Management:** Full CRUD (Create, Read, Update, Delete) functionality for opportunities.
- **Data Isolation:** Admins can only view, edit, and delete the opportunities they have created.
- **Dynamic UI:** All data operations happen seamlessly via JSON APIs without requiring page refreshes.

## Technologies Used
- Python 3  
- Flask  
- Flask‑SQLAlchemy (Database ORM)  
- Flask‑Login (Session management)  
- Flask‑CORS  
- Werkzeug (Password hashing)  
- ItsDangerous (Secure token generation)  

## Setup and Installation

Follow these steps to run the application locally on your machine.

### 1. Clone the repository
```bash
git clone https://github.com/MaheshJakkula003/Admin-Portal.git
cd Admin-Portal
```

### 2. Create and activate a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
The SQLite database (`database.db`) will automatically generate upon running if it does not already exist.
```bash
python app.py
```
Open your browser at: `http://127.0.0.1:5000`

---

## Project Structure
- `app.py` → Main Flask app entry point  
- `routes.py` → Application routes & API endpoints  
- `models.py` → Database models (Admin, Opportunity)  
- `templates/` → HTML templates  
- `static/` → CSS/JS files  
- `config.py` → Configuration settings  

---

## Environment Variables (Optional)
The app uses a default development secret key, but for production, you can set these environment variables:
```bash
SECRET_KEY=your_secret_here
DATABASE_URL=sqlite:///database.db
```

---

##  Testing the Application
To verify the application works as intended, follow these manual testing steps:
1. Click **Sign Up** to create a new Admin account.  
2. Log in with your new credentials and test the **Remember Me** functionality.  
3. Navigate to the **Opportunities** tab to add, edit, and delete opportunities.  
4. Log out and test the **Forgot Password** token generation (the secure token will print in your terminal).  
```

---
