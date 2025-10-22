# GrowthPlug Facebook Page Manager

This is a Django-based web application that allows users to manage their Facebook pages after authenticating with their Facebook account.

## Features

- Facebook user authentication
- View and update Facebook page information

## Installation

1. Clone the repository.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the application at `http://localhost:8000`.
2. Log in using your Facebook account.
3. You will be redirected to a page where you can view and manage your Facebook page information.

## Project Structure

- `growthplug/`: Contains the core project settings.
- `applications/dashboard/`: The main application that handles Facebook authentication and page management.
- `templates/`: Contains the HTML templates for the application.
- `static/`: Contains static files like CSS and JavaScript.
- `manage.py`: The command-line utility for Django.
- `requirements.txt`: A list of the project's Python dependencies.

## Dependencies

- Django
- Django REST Framework
- django-rest-auth
- facebook-sdk
- django-extensions
- requests
