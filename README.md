**Admin Portal**

*   **Authentication:** Secure Admin Sign Up, Login (with "Remember Me" session persistence), and Forgot Password (with secure, 1-hour expiring tokens).
*   **Opportunity Management:** Full CRUD (Create, Read, Update, Delete) functionality for opportunities.
*   **Data Isolation:** Admins can only view, edit, and delete the opportunities they have created.
*   **Dynamic UI:** All data operations happen seamlessly via JSON APIs without requiring page refreshes.

## Technologies Used

*   Python 3
*   Flask
*   Flask-SQLAlchemy (Database ORM)
*   Flask-Login (Session management)
*   Flask-CORS
*   Werkzeug (Password hashing)
*   ItsDangerous (Secure token generation)

## Setup and Installation

Follow these steps to run the application locally on your machine.

**1. Clone the Repository**
```bash
git clone [https://github.com/MaheshJakkula003/Admin-Portal.git](https://github.com/MaheshJakkula003/Admin-Portal.git)
cd Admin-Portal

**2. Create a Virtual Environment**
It is highly recommended to use a virtual environment to manage dependencies.

Bash
python -m venv venv

**3. Activate the Virtual Environment**

Windows:

Bash
venv\Scripts\activate
macOS and Linux:

Bash
source venv/bin/activate

**4. Install Dependencies**
Install all required Python packages listed in the requirements file.

Bash
pip install -r requirements.txt
5. Run the Application
Start the Flask development server. The SQLite database (database.db) will automatically generate upon running if it does not already exist.

Bash
python app.py

**6. Access the Portal**
Open your web browser and navigate to: http://127.0.0.1:5000/

Testing the Application
Start by clicking "Sign Up" to create a new Admin account.

Log in with your new credentials. Test the "Remember Me" functionality.

Navigate to the "Opportunities" tab to add, edit, and delete opportunities.

Log out and test the "Forgot Password" token generation in the terminal.

Note on Dependencies: Ensure that requirements.txt is present in your repository. If you haven't generated it yet, run pip freeze > requirements.txt while your virtual environment is active, and commit the file to GitHub.


This version uses proper Markdown syntax (` ```bash ` for code blocks, `##` for headings, and `*` for bullet points) so GitHub can read and style it correctly.
