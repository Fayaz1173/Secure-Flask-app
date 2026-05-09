# Cloud Deployment Report: Flask Authentication Project on Railway with SendGrid Email Verification

## 1. Introduction

This project is a secure Flask-based authentication web application deployed on the cloud using Railway. The application includes user registration, login, OTP email verification, session handling, password hashing, CSRF protection, and Google reCAPTCHA integration. SendGrid was integrated as the email service provider for reliable OTP email delivery.

The project demonstrates deployment of a modern Flask web application in a cloud environment with secure authentication and third-party email service integration.

---

# 2. Objectives

The main objectives of this project were:

- Deploy a Flask application to the cloud
- Implement secure user authentication
- Integrate OTP-based email verification
- Configure SendGrid for transactional email delivery
- Use Railway for cloud hosting and deployment
- Secure the application using sessions, CSRF protection, password hashing, and reCAPTCHA

---

# 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Flask | Web framework |
| Flask-WTF | Form handling and CSRF protection |
| Flask-Bcrypt | Password hashing |
| SQLAlchemy | Database ORM |
| SendGrid | OTP email delivery |
| Railway | Cloud deployment platform |
| GitHub | Version control and deployment source |
| Gunicorn | Production WSGI server |
| Google reCAPTCHA | Bot protection |

---

# 4. Project Features

The Flask application includes:

- User Registration
- Secure Login System
- OTP Email Verification
- Password Hashing using Bcrypt
- Session Management
- CSRF Protection
- Google reCAPTCHA Verification
- Secure Logout
- Database Storage using SQLite

---

# 5. Railway Cloud Deployment

## 5.1 Repository Preparation

The Flask project was prepared for deployment by creating the following deployment files:

### `requirements.txt`

Used to install all required dependencies automatically.

Example packages:


Flask,
gunicorn,
Flask-WTF,
Flask-Bcrypt,
Flask-SQLAlchemy,
sendgrid,
email-validator.

<img width="1918" height="902" alt="Screenshot 2026-05-09 114446" src="https://github.com/user-attachments/assets/947f9eb0-1824-449c-9842-fe2663afd24c" />

<img width="1910" height="856" alt="Screenshot 2026-05-09 114555" src="https://github.com/user-attachments/assets/bf7c7b68-bdc1-4565-a535-65ae43da88c4" />

