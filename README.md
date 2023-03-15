# Authentication API with Django and REST framework using JWT
This is an authentication API built with Django and the Django REST framework. The API provides authentication functionality using JSON Web Tokens (JWTs) for user authorization.

# Features
* User registration and authentication
* Password reset functionality (Email Verification)
* Password Change functionality
* Token authentication using JWTs
* Endpoint for refreshing access tokens
* Token revocation for logged out or inactive users


# Installations
* clone the repo
* pip install -r requirements.txt
* migrate the database (python manage.py migrate)
* create superuser
* Run the server

# Few Modifications
* Before running this project configure your email .env file

# API ENDPOINTS
* BaseUrl: 'api/user/'
* Other Endpoints:
* 'register/'
* 'login/'
* 'profile/'
* 'changepassword/'
* 'send-reset-password-email/'
* 'changeprofile/'
* 'reset-password/' [Sent to your Email]

# Technologies Used
* Python
* Django
* Django Rest Framework
* JWT Authentication

# Contribution
Contributions are always welcome! If you have any suggestions or find any bugs please submit an issue or a pull request.
