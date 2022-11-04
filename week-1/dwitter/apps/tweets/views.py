from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# First Session: We wish to create a view that just greets the user and says "Welcome to Dwitter"
# We also want to make sure that only logged in users can access this view, and if a user is not logged in
# they should be redirected to the login page
# We can do this by using the login_required decorator from django.contrib.auth.decorators (see https://docs.djangoproject.com/en/4.1/topics/auth/default/#the-login-required-decorator)
# This decorator will check if the user is logged in, and if they are not, it will redirect them to the login page
# We can also specify the url to redirect to by passing in the login_url parameter to the decorator

# The login page is at /accounts/login/ but we don't want to hardcode this url in our code
# We can use the reverse_lazy function from django.urls to get the url for the login page by looking up its view name "login"

# We implement the view as a function that takes in a request object and returns a response object
# We use our generic_message.html template to render the message to the user, this template takes in a context variable "content"
# which is the message we want to show to the user
# We can pass this context variable to the template by passing it to the render function as a dictionary
# The render function will then render the template with the context variables and return a response object

# ADDITION: decorate view with login_required and pass in the login_url parameter

def index(request):
    # ADDITION: render a response greeting the user (mention their username) and saying "Welcome to Dwitter"
    # you can get the username from the request.user object
    # you can use the generic_message.html template to render the message (if you have implemented it)
    # you can render the results using the render function
    pass # remove this line and replace it with your code