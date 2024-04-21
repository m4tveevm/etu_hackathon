# LK Assistant

[![Django CI/CD testing](https://github.com/m4tveevm/etu_hackathon/actions/workflows/django.yml/badge.svg)](https://github.com/m4tveevm/etu_hackathon/actions/workflows/django.yml)

## Overview

LK Assistant is a Django-based application designed to enhance the experience of students and staff at educational institutions by providing automated tools for managing personal academic information and resources. This application integrates seamlessly with the existing university systems to offer a range of features from schedule management to session data tracking.

## Features

- **User Authentication**: Secure login and registration system for managing user accounts.
- **Schedule Integration**: Automatically fetch and display academic schedules.
- **Real-Time Notifications**: Receive updates on academic events, deadlines, and important notices.
- **Profile Management**: Users can update their profiles with academic and personal information.
- **Secure Data Handling**: All user data, including passwords, are encrypted and securely stored.

## Technologies

LK Assistant is built using the following technologies:
- **Django 4.2.4**: For the backend and application framework.
- **SQLite**: Default database for development and testing.
- **Bootstrap**: For responsive frontend design.
- **Requests and BeautifulSoup**: Used for parsing and interacting with external academic systems.

## Installation

To set up a local development environment, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/m4tveevm/etu_hackathon.git
   ```
2. Navigate to the project directory:
   ```bash
   cd etu_hackathon
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations to create the database schema:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. Open a web browser and navigate to `http://127.0.0.1:8000/` to view the application.

## Usage

After starting the server, you can:
- Register a new user account.
- Login with your credentials.
- Update your profile.
- View your academic schedule.

## Contributing

Contributions to LK Assistant are welcome. Please follow these steps to make a contribution:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
