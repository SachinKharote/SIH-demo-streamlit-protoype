# 🌱 SIH Demo Streamlit  

A demo web application built with **Streamlit** for SIH (Smart India Hackathon) showcasing a secure authentication system and feature integration.  

This project implements:  
- ✅ User Registration & Login  
- ✅ SQLite Database for persistence  
- ✅ Password Hashing (SHA256)  
- ✅ Email Verification with SendGrid  
- ✅ Token-based account verification  
- ✅ Modular, extendable codebase  

---

## 📂 Project Structure  

SIH-demo-streamlit/
│
├── app.py # Main Streamlit app
├── auth.py # Authentication logic
├── requirements.txt # Python dependencies
├── users.db # SQLite database (auto-created)
└── README.md # Project documentation


---

## ⚡ Features  

- **User Registration** → Stores name, email, password (hashed), and generates a token.  
- **Email Verification** → SendGrid email with verification link.  
- **Login System** → Only verified users can log in.  
- **Database** → SQLite with `id, name, email, password, verified, token`.  

---

## 🔧 Installation & Setup  

```bash
# Clone repo
git clone https://github.com/<your-username>/SIH-demo-streamlit.git
cd SIH-demo-streamlit

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Set SendGrid API key
export SENDGRID_API_KEY="your_api_key_here"    # Mac/Linux
set SENDGRID_API_KEY=your_api_key_here         # Windows

# Run app
streamlit run app.py

📧 Email Verification
Registration sends verification mail via SendGrid.
User must click the link to activate account.
Only verified users can log in.

📜 Requirements

streamlit
sqlite3 (built-in)
sendgrid
hashlib

🚀 Future Scope

Role-based access control
Crop recommendation/weather integration
Cloud deployment (Heroku, AWS, Streamlit Cloud)

