import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ksach320@gmail.com"
SENDER_PASSWORD = "Sachin@#2024."  # Use app password if using Gmail

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("Login successful!")
    server.quit()
except Exception as e:
    print("Failed:", e)
