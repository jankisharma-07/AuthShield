# AuthShield - Flask Authentication App

🔐 **AuthShield** is a Flask-based authentication system with:

- Secure login with brute-force detection
- Signup with password suggestions
- User-specific login history
- modern UI

## Features

1. **Login & Signup** with secure password checking
2. **Suggested Passwords** using a smart generator
3. **Dashboard** showing only your login history
5. **Brute-force detection** and temporary account lock

## Installation

```bash
git clonehttps://github.com/jankisharma-07/AuthShield.git
cd AuthShield
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
python app.py
