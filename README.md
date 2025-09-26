🌱 SIH Demo Streamlit

A demo web application built with Streamlit for SIH (Smart India Hackathon) showcasing a secure authentication system and basic feature integration.

This project implements:
✅ User Registration & Login
✅ SQLite Database for persistence
✅ Password Hashing (SHA256)
✅ Email Verification with SendGrid
✅ Token-based account verification
✅ Modular, extendable codebase

📂 Project Structure

SIH-demo-streamlit/
│
├── app.py               # Main Streamlit app
├── auth.py              # Authentication logic
├── requirements.txt     # Python dependencies
├── users.db             # SQLite database (auto-created)
└── README.md            # Project documentation

⚡ Features

User Registration
Stores name, email, password (hashed).
Generates a unique token for email verification.

Email Verification
Uses SendGrid to send a verification email.
Users must verify their email before login.

Login System
Allows only verified users to login.
Uses hashed passwords for security.

Database
SQLite with a users table.
Columns: id, name, email, password, verified, token.

🔧 Installation & Setup

Clone the repo:
git clone https://github.com/<your-username>/SIH-demo-streamlit.git
cd SIH-demo-streamlit

Create & activate a virtual environment:
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

Install dependencies:
pip install -r requirements.txt

Set up SendGrid API Key:
export SENDGRID_API_KEY="your_api_key_here"    # Mac/Linux
set SENDGRID_API_KEY=your_api_key_here         # Windows

Run the app:
streamlit run app.py

📧 Email Verification
On registration, a verification mail is sent via SendGrid.
Users must click the link to activate their account.
Only verified users can log in.

📜 Requirements

See requirements.txt for all dependencies. Key libraries:
streamlit
sqlite3 (built-in)
sendgrid
hashlib

🚀 Future Scope
Add role-based access control.
Expand features beyond authentication (e.g., weather or crop planner module).
Deploy on cloud (Heroku, AWS, or Streamlit Cloud).

🤝 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.
