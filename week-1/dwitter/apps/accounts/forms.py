from django import forms
from django.utils.translation import gettext_lazy as _


# First Session: We wish to create a signup form that asks for the user's username, firstname, lastname, email, and password
# Going through django's documentation, we see that django.contrib.auth provides a set of stock forms
# one of which is UserCreationForm https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
# This form, already has the username, and password fields, and implements the logic to validate the data
# and create a user. So we only need a way to add the first name, last name, and email fields to this form
# We can do this by subclassing the UserCreationForm and adding the fields we want
# By subclassing, we also bring in all the logic that the UserCreationForm already has so we don't have to
# re-implement it ourselves
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    # ADDITION: add first_name, last_name, and email fields (based on the underlying User model)

    
    
    def save(self, commit=True):
        # We override the save method to save the first_name, last_name, and email fields
        # We do this because the UserCreationForm doesn't save these fields 
        # by default and doesn't account for field additions (i.e it doesn't know about the first_name, last_name, and email fields)

        # We can do this by calling the save method of the parent class (UserCreationForm) first (with commit=False) 
        # which creates a user instance without saving it and sets its username and password 
        # then we can set the instance's first_name, last_name, and email fields manually and then save it
        # if commit (the argument to this method) is True
        
        user = super().save(commit=False)
        # self.cleaned_data is a dictionary of the form data that has been cleaned and validated
        # we can access the first_name, last_name,
        # and email fields from this dictionary and set them on the user instance
        # ADDITION: set first_name, last_name, and email fields on user instance

        # ADDITION: save user instance if commit is True
        
        return user # forms are supposed to return the created object instance
    
    # Now we have a form which has the username, password1, password2, first_name, last_name, and email fields
    # and it implements the logic to validate the data and create a user
    # So we can use this form in our signup view to create a new user (see dwitter/apps/accounts/views.py)

