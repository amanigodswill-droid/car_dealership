# Mipango Car Dealership

## Project Description
Mipango Car Dealership is a web application developed using Django. It provides a platform where users can browse cars for sale, view vehicle details, register accounts, and manage car listings. Registered sellers can manage their listings and respond to purchase requests.

## Features
- User registration, login, and logout.
- Password reset through email.
- Create, view, update, and delete car listings.
- Upload and display car images.
- Seller profiles with contact information.
- Browse available cars and view their details.
- Submit purchase requests.
- Manage purchase requests and update their status.
- Responsive user interface.

## Technologies Used
- Python
- Django
- HTML and CSS
- SQLite
- Git and GitHub

## Installation and Setup
1. Clone the repository:

   ```bash
   git clone https://github.com/amanigodswill-droid/car_dealership
   ```

2. Navigate into the project directory:

   ```bash
   cd car_dealership
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment on Windows Git Bash:

   ```bash
   source .venv/Scripts/activate
   ```

5. Install Django:

   ```bash
   pip install "Django<5.3" Pillow
   ```

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Open the application in your browser:
   `http://127.0.0.1:8000/`

## Email Configuration
Email settings are configured through Django settings. Configure your email credentials securely using environment variables before using email features in another environment.

## Running Tests
Run Django's system check:

```bash
python manage.py check
```

## Project Purpose
This project was developed as an end-of-module capstone to demonstrate practical skills in Django development, database management, authentication, CRUD operations, and web application design.