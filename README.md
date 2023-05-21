# Email Service And Management System

This is an Email Service And Management System, a web application built with Django. It allows users to send, receive, and manage their emails within the system.

## Features

- User authentication: Users can create an account, log in, and log out.
- Inbox: Users can view and manage their received emails.
- Sent Mail: Users can view their sent emails.
- Archive: Users can archive emails to keep them organized.
- Starred: Users can mark emails as starred for easy access.
- Trash: Deleted emails are moved to the trash and can be restored or permanently deleted.
- Spam Filtering: The system automatically detects spam emails and marks them accordingly.
- Real-time Updates: WebSocket integration enables real-time updates for new email notifications.

## Prerequisites

Before running the application, make sure you have the following prerequisites:

- Python (3.7 or higher)
- Django (3.2 or higher)
- Redis server (for WebSocket support)
- Cloudinary account (for email attachments)

## Installation

1. Clone the repository:

```
git clone https://github.com/rohanphulkar/email-management-system.git
```

2. Change into the project directory:

```
cd email-management-system
```

3. Install the Python dependencies:

```
pip install -r requirements.txt`
```

4. Set up the database:

```
python manage.py migrate
```

5. Create a superuser:

```
python manage.py createsuperuser
```

6. Configure Cloudinary:

- Sign up for a Cloudinary account at https://cloudinary.com.
- Obtain your Cloudinary API credentials.
- Update the .env file with your Cloudinary credentials.

7. Start the Redis server:

```
redis-server
```

8. Start the Django development server:

```
python manage.py runserver
```

#### Access the application in your web browser at http://localhost:8000.

### URLs

The project includes the following URLs for the "emails" app:

- `GET /`: Displays the list of emails in the user's inbox.
- `GET /<id>/`: Displays a specific email with the given ID.
- `POST /star/<id>/`: Stars or unstars an email with the given ID.
- `POST /archive/<id>/`: Archives or unarchives an email with the given ID.
- `POST /delete/<id>/`: Deletes an email with the given ID (moves it to the trash).
- `POST /restore/<id>/`: Restores a deleted email with the given ID.
- `POST /not-spam/<id>/`: Marks a spam email as not spam.
- `POST /permanent-delete/`: Permanently deletes all emails in the trash.

Please note that these URLs are specific to the "emails" app within the project. Make sure to include the appropriate app namespace or modify the URLs according to your project's URL configuration.

### Configuration

1. Create a `.env` file in the project root directory.
2. Add the following environment variables to the `.env` file:

```
CLOUDINARY_CLOUD_NAME="your_cloudinary_cloud_name"
CLOUDINARY_API_KEY="your_cloudinary_api_key"
CLOUDINARY_API_SECRET="your_cloudinary_api_secret"
DB_NAME="your_database_name"
DB_USER="your_database_username"
DB_HOST="your_database_host"
DB_PASSWORD="your_database_password"
DB_PORT=your_database_port
SMS_API_KEY="your_sms_api_key"
REDIS_DB="your_redis_db_url"
```
