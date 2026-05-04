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
