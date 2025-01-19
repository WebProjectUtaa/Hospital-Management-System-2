# Hospital Management System

This project is a backend implementation for a hospital management system. It is designed as a microservices architecture and uses Sanic for the API framework and MySQL for the database. Below are details about the project structure, setup, and how to use it.

---

## Features

- **Admin Management**: Manage hospital administrators.
- **Authentication**: User login and authentication via `auth_service`.
- **Appointment System**: Handle patient appointments with doctors.
- **Doctor & Nurse Management**: Manage doctors, nurses, and other staff.
- **Patient Management**: Register and manage patient details.
- **Lab Test Management**: Track and record lab tests.
- **Notifications**: Manage system-generated notifications.

---

## Project Structure

```
Hospital-Management-System-2
├── admin_service
├── appointment_service
├── auth_service
├── doctor_service
├── lab_test_service
├── login_service
├── notification_service
├── nurse_service
├── patient_service
├── registration_service
├── utils
```

### Key Files

- **`start_services.ps1`**: Script to start all microservices.
- **`requirements.txt`**: Contains Python dependencies.
- **`.env`**: Stores environment variables (ensure sensitive data is excluded from version control).

---

## Setup Instructions

### Prerequisites

- Python 3.10.11
- MySQL database
- Git

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/WebProjectUtaa/Hospital-Management-System-2.git
   cd Hospital-Management-System-2
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file:

   - Update the file with your MySQL credentials and other environment variables.

5. Initialize the database:

   - Import the MySQL dump file provided in the project.

   ```bash
   mysql -u <username> -p < database_name < dumpfile.sql
   ```

6. Start the services:

   ```bash
   powershell ./start_services.ps1
   ```

---

## API Endpoints

Each service has its own set of endpoints. Here is an example for `auth_service`:

### Auth Service

- **POST /login**: Authenticate a user and generate a token.
- **POST /register**: Register a new user.
- **GET /users**: Retrieve all users (admin only).



---

## Contribution Guidelines

- Ensure code follows PEP8 standards.
- Document functions and classes clearly.
- Use feature branches for development and submit pull requests for review.

---

##

