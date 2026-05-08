from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import time
import os
import secrets
import re
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Secret key setup for Lambda readiness
def get_secret_key():
    # Attempt to get secret key from environment
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        return env_key
    # Fallback to random key for local development
    return secrets.token_hex(32)

app.secret_key = get_secret_key()

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE="Lax"
)

app.permanent_session_lifetime = timedelta(minutes=30)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(10))
    otp_expiry = db.Column(db.Float)
    is_verified = db.Column(db.Integer, default=0)

# Create tables
with app.app_context():
    db.create_all()

def verify_recaptcha(response_token):
    payload = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": response_token
    }
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data=payload
    )
    result = response.json()
    return result.get("success", False)

def send_otp_email(to_email, otp):
    if not SENDGRID_API_KEY:
        print("ENV email config missing")
        return False

    message = Mail(
        from_email="noreply@secureflaskapp.com",
        to_emails=to_email,
        subject="Email Verification OTP",
        plain_text_content=f"Your OTP is {otp}. It expires in 5 minutes."
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print("OTP email sent successfully")
        return True
    except Exception as e:
        print("EMAIL ERROR:", e)
        return False

def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain special character."
    return True, ""

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        recaptcha_response = request.form.get("g-recaptcha-response")
        if not verify_recaptcha(recaptcha_response):
            return render_template("register.html", message="Invalid reCAPTCHA.", site_key=RECAPTCHA_SITE_KEY)

        email = request.form.get("email").strip().lower()
        password = request.form.get("password")
        valid_password, password_message = is_strong_password(password)

        if not valid_password:
            return render_template("register.html", message=password_message, site_key=RECAPTCHA_SITE_KEY)

        hashed_password = generate_password_hash(password)
        otp = generate_otp()
        expiry = time.time() + 300

        try:
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                if existing_user.is_verified == 1:
                    message = "User already exists."
                    return render_template("register.html", message=message, site_key=RECAPTCHA_SITE_KEY)
                else:
                    existing_user.password = hashed_password
                    existing_user.otp = otp
                    existing_user.otp_expiry = expiry
                    db.session.commit()
            else:
                new_user = User(email=email, password=hashed_password, otp=otp, otp_expiry=expiry, is_verified=0)
                db.session.add(new_user)
                db.session.commit()

            email_sent = send_otp_email(email, otp)

            if not email_sent:
                # Rollback/delete the user if email failed
                user_to_delete = User.query.filter_by(email=email, is_verified=0).first()
                if user_to_delete:
                    db.session.delete(user_to_delete)
                    db.session.commit()

                return render_template("register.html", message="Failed to send OTP email.", site_key=RECAPTCHA_SITE_KEY)

            return redirect(url_for("verify", email=email))

        except Exception as e:
            return render_template("register.html", message=f"Error: {e}", site_key=RECAPTCHA_SITE_KEY)

    return render_template("register.html", site_key=RECAPTCHA_SITE_KEY)

@app.route("/verify/<email>", methods=["GET", "POST"])
def verify(email):
    message = ""
    if request.method == "POST":
        user_otp = request.form.get("otp")

        user = User.query.filter_by(email=email).first()

        if user:
            if time.time() > user.otp_expiry:
                message = "OTP expired."
            elif user_otp == user.otp:
                user.is_verified = 1
                user.otp = None
                user.otp_expiry = None
                db.session.commit()
                return redirect(url_for("login"))
            else:
                message = "Invalid OTP."
        else:
            message = "User not found."

    return render_template("verify.html", message=message, email=email)

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        # -----------------------
        # RECAPTCHA VALIDATION
        # -----------------------
        recaptcha_response = request.form.get("g-recaptcha-response")
        if not recaptcha_response:
            return render_template("login.html", message="Please complete the reCAPTCHA.", site_key=RECAPTCHA_SITE_KEY)

        if not verify_recaptcha(recaptcha_response):
            return render_template("login.html", message="Invalid reCAPTCHA.", site_key=RECAPTCHA_SITE_KEY)

        # -----------------------
        # LOGIN LOGIC
        # -----------------------
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if user.is_verified == 0:
                message = "Please verify your email first."
            elif check_password_hash(user.password, password):
                session.clear()
                session.permanent = True
                session["user"] = email
                return redirect(url_for("dashboard"))
            else:
                message = "Invalid credentials."
        else:
            message = "User not found."

    return render_template("login.html", message=message, site_key=RECAPTCHA_SITE_KEY)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)