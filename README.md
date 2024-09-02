
Here’s a README.md file that you can use for the above social networking API project:


# Social Networking API

This project is a social networking application built using Django Rest Framework (DRF). The application allows users to sign up, log in, search for other users, send/accept/reject friend requests, and view lists of friends and pending friend requests.

## Features

- **User Signup**: Users can sign up with their email (case-insensitive) and password,first name and last name
- **User Login**: Users can log in using their email (case-insensitive) and password.
- **Search Users**: Users can search for other users by email or name.
- **Send Friend Request**: Authenticated users can send friend requests to other users.
- **Accept/Reject Friend Request**: Users can accept or reject received friend requests.
- **List Friends**: Users can view a list of their friends (users who have accepted their friend requests).
- **List Pending Friend Requests**: Users can view a list of pending friend requests they have received.
- **Rate Limiting**: Users cannot send more than 3 friend requests within a minute.

## Installation

### Prerequisites

- Python 
- Django
- Django Rest Framework
-djangorestframework-simplejwt
- Any database of your choice

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd socialnetwork



2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:

pip install -r requirements.txt

4. Set up the database:

By default, the project uses SQLite, but you can configure another database in the settings.py file.

python manage.py migrate


5. Create a superuser (optional, for admin access):

python manage.py createsuperuser


6.Run the development server:

python manage.py runserver

7.Access the application:

Open your browser and navigate to http://127.0.0.1:8000/.



API Endpoints
Authentication
Signup: POST /api/register/

Request Body: { "firstname": "firstname", "lastname":"lastname" ,email": "user@example.com", "password": "password" }
Response: 201 Created if successful, with user details.

Login: POST /api/token/

Request Body: { "email": "user@example.com", "password": "password" }
Response: 200 OK with JWT tokens.

User Management
Search Users: GET /api/search-users/?q=<keyword>
Search users by email or name (case-insensitive).
Response: 200 OK with a list of matching users.

Friend Requests
Send Friend Request: POST /api/friend-request/send/

Request Body: { "to_user": "<user_id>" }
Response: 201 Created if successful.


Accept Friend Request: PUT /api/friend-request/accept/<id>/

Response: 200 OK if successful.


Reject Friend Request: PUT /api/friend-request/reject/<id>/

Response: 200 OK if successful.


List Friends: GET /api/friends/

Response: 200 OK with a list of friends.


List Pending Friend Requests: GET /api/friend-request/pending/

Response: 200 OK with a list of pending friend requests.



