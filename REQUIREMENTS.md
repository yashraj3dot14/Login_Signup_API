# User Registration & Login API
## Functionality: User registration,Login with know Auth Token,password reset and change

###Registration Functionality:
It is achieved with Django Custom user model, Email will be the username
other fields are first_name, last_name, mobile

###Login Functionality
It  has been implemented through Knox Aut token,once user will be login Auth token will be created for userid

###Change password and password reset
User can change his/her password, for reset password, it can be implemented through mail,
Email functionality is not giving 100% accuracy here.


###Endpoints
http://127.0.0.1:8000/api/signup/  ==>User Registration
http://127.0.0.1:8000/api/signin/ Login and generating Token
http://127.0.0.1:8000/api/change_password/ To change password
http://127.0.0.1:8000/api/password_reset/ Reset password through email