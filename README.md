# boko-hacks-25
Test repo for Texas State's 2025 Bokohacks - A Cybersecurity Challenge Platform

## Overview
This project is a web application designed to help students learn about common web security vulnerabilities through hands-on practice. It includes various challenges focusing on SQL injection, XSS, access control vulnerabilities, and authentication bypass techniques.

## Requirements
- Python 3.8 or higher --> [Download Python](https://www.python.org/downloads/)
- Pip (Python package installer)
- SQLite --> [Download SQLite](https://www.sqlite.org/download.html)
- Modern web browser (Chrome/Firefox recommended)
- Text editor or IDE (VS Code recommended)

## Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/yourusername/boko-hacks-25.git
cd boko-hacks-25
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database and create test data:
```bash
python run_migration.py
```

5. Start the application:
```bash
python app.py
```

6. Open http://localhost:5000 in your browser

## Test Accounts
After running migrations, the following test accounts are available:

Regular Users:
- Username: alice, Password: password123
- Username: bob, Password: password456
- Username: charlie, Password: password789

Admin User (after fixing vulnerabilities):
- Username: admin, Password: password

## Available Challenges

### 1. Notes App
- Test for XSS and SQL injection vulnerabilities
- Practice finding access control issues
- Search functionality with SQL injection possibilities
- Ability to view and manipulate other users' notes

### 2. Admin Access Control
- Test authentication bypass through SQL injection
- Vulnerable admin login system
- Insecure registration process
- Practice implementing password hashing
- Access control vulnerabilities in admin dashboard

### 3. File Upload (Coming Soon)
- Practice bypassing file upload restrictions
- Test for file type vulnerabilities

### 4. Chat Room (Coming Soon)
- Find vulnerabilities in real-time communication
- Test for XSS in chat messages

### 5. REST API (Coming Soon)
- Test API endpoints for security misconfigurations
- Practice API exploitation techniques

## Vulnerabilities to Find
1. SQL Injection in:
   - Note search functionality
   - Admin login
   - User registration

2. Authentication Bypass:
   - Admin panel access
   - User impersonation
   - Missing password hashing

3. Access Control Issues:
   - Unauthorized note access
   - Admin privilege escalation
   - Cross-user data manipulation

## Development Notes
- The application uses Flask for the backend
- Two separate SQLite databases:
  - Main database (boko_hacks.db) for user data and notes
  - Admin database (admin_database.db) for admin authentication
- Frontend uses vanilla JavaScript and CSS
- Intentionally vulnerable for educational purposes

## Security Notice
This application contains intentional security vulnerabilities for educational purposes. DO NOT use any real credentials or sensitive information while testing. This application should only be run locally in a controlled environment.

## Contributing
1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request

## License
MIT License - See LICENSE file for details