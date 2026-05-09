# Comprehensive Project & Security Report: Secure Flask Authentication App

## Project Overview
This project is a secure, scalable web application built with Flask (Python), featuring a robust user authentication system. The application emphasizes security best practices, providing a complete flow for user registration, login, and session management. Key features include strong password policies, Email-based One-Time Passwords (OTP) for Multi-Factor Authentication (MFA), and Google reCAPTCHA integration to prevent automated bot attacks.

## Technology Stack
- **Backend Framework**: Flask (Python)
- **Database**: SQLite (managed via SQLAlchemy ORM)
- **Authentication & Security**: Werkzeug (for robust password hashing), Google reCAPTCHA API, Python `secrets` module
- **Email Delivery**: SMTP for automated OTP email delivery
- **Frontend**: HTML5, Vanilla CSS (featuring a modern glassmorphism design), and SweetAlert2 (for interactive popups)
- **Environment Management**: `python-dotenv` for securely managing sensitive credentials

## Project Workflow

1. **User Registration**:
   - The user submits their email and a strong password via the registration form.
   - A Google reCAPTCHA challenge is verified to prevent bot submissions.
   - The server validates the password strength (length, uppercase, lowercase, numbers, special characters).
   - If valid, the user's password is cryptographically hashed, and a new record is created in the database (marked as unverified).
   - A 6-digit One-Time Password (OTP) is generated and sent to the user's email via SMTP.

2. **Email OTP Verification**:
   - The user is redirected to a verification page.
   - They must enter the 6-digit OTP received via email within a 5-minute expiration window.
   - Upon successful verification, the user's account is marked as active in the database.

3. **Secure Login**:
   - The active user enters their credentials on the login page.
   - A Google reCAPTCHA challenge is again verified.
   - The server verifies that the email exists, the account is verified, and the provided password matches the hashed password in the database.
   - Upon success, a secure, HTTP-only session is established. A dynamic popup (SweetAlert2) confirms the successful login process.

4. **Dashboard Access & Session Management**:
   - The user gains access to protected routes (like the Dashboard).
   - The session remains active for up to 30 minutes.
   - Cache-control headers are strictly enforced so that sensitive pages cannot be accessed via the browser's "Back" button after logout.

5. **Logout**:
   - The user clicks logout, destroying the session securely on the server side and redirecting them back to the login page.

---

## I. Current Security Features Added in the App


1. **Password Hashing**: The application uses `werkzeug.security` (`generate_password_hash` and `check_password_hash`) to securely hash and verify passwords instead of storing them in plain text.
2. **Parameterized Database Queries**: SQLite queries use parameter substitution (e.g., `WHERE email = ?`) which effectively prevents SQL Injection attacks.
3. **Password Complexity Enforcement**: The `is_strong_password` function ensures that passwords meet minimum strength requirements (at least 8 characters, uppercase, lowercase, numbers, and special characters).
4. **Secret Key Generation**: The app generates a strong, random 32-byte hexadecimal secret key using the `secrets` module, preventing predictable session signatures.
5. **Secure Session Management**: 
   - Sessions are set to expire after 30 minutes of inactivity (`permanent_session_lifetime`).
   - `SESSION_COOKIE_HTTPONLY=True` prevents client-side JavaScript from accessing the session cookie, mitigating XSS attacks.
   - `SESSION_COOKIE_SAMESITE="Lax"` provides baseline protection against Cross-Site Request Forgery (CSRF).
   - `session.clear()` is called appropriately during login and logout to prevent session fixation.
6. **Email OTP Verification**: The app implements a form of Multi-Factor Authentication (MFA) by requiring users to verify their email address via a 6-digit OTP that expires in 5 minutes before the account becomes active.
7. **Bot Protection**: Google reCAPTCHA is integrated into both the registration and login flows to prevent automated brute-forcing and spam registrations.
8. **Environment Variables**: Sensitive configuration data such as email credentials and API keys are stored in a `.env` file instead of being hardcoded in the source code.
9. **No-Cache Headers**: An `@app.after_request` hook explicitly prevents browsers from caching application pages (`Cache-Control: no-store`), ensuring that sensitive information (like the dashboard) cannot be viewed by hitting the browser's "Back" button after logging out.
10. **Input Normalization**: Email inputs are stripped of whitespace and converted to lowercase, which prevents duplicate accounts caused by case sensitivity and reduces edge-case vulnerabilities.

---

<img width="1912" height="880" alt="Screenshot 2026-05-09 102753" src="https://github.com/user-attachments/assets/42fe0fc1-8697-4c43-bcc6-b43d16063edf" />

<img width="1919" height="883" alt="Screenshot 2026-05-09 102711" src="https://github.com/user-attachments/assets/39801847-5c32-474b-96d2-833137403340" />

<img width="1901" height="967" alt="Screenshot 2026-05-09 102652" src="https://github.com/user-attachments/assets/9942249a-e6d8-4d86-8293-2a42e8bd60a6" />

<img width="1917" height="873" alt="Screenshot 2026-05-09 102736" src="https://github.com/user-attachments/assets/a1451a41-eec6-48a7-a43b-710d654f0153" />

<img width="1901" height="972" alt="Screenshot 2026-05-09 102828" src="https://github.com/user-attachments/assets/c6bc22a2-118f-4481-89de-0f777d11c237" />



