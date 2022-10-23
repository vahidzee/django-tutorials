from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

# We wish to create a signup form that asks for the user's username, firstname, lastname, email, and password
# Going through django's documentation, we see that django.contrib.auth provides a set of stock forms
# one of which is UserCreationForm https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
# This form, already has the username, and password fields, and implements the logic to validate the data
# and create a user. So we only need a way to add the first name, last name, and email fields to this form
# We can do this by subclassing the UserCreationForm and adding the fields we want
# By subclassing, we also bring in all the logic that the UserCreationForm already has so we don't have to
# re-implement it ourselves


class SignupForm(UserCreationForm):
    # based on the underlying User model
    first_name = forms.CharField(label=_("First name"), max_length=150, required=False)
    last_name = forms.CharField(label=_("Last name"), max_length=150, required=False)
    email = forms.EmailField(required=False)

    # Now we have a form which has the username, password1, password2, first_name, last_name, and email fields
    # and it implements the logic to validate the data and create a user
    # So we can use this form in our signup view to create a new user (see dwitter/apps/accounts/views.py)
