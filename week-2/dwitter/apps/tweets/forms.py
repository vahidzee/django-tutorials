# # Uncomment all the lines in this file once you have created your tweet model in dwitter/apps/tweets/models.py
# # and finished the admin configuration in dwitter/apps/tweets/admin.py (and checked that everything works in the admin site)
# # to start working on the views for the tweet model


# from django import forms
# from django.utils.translation import gettext_lazy as _
# from .models import Tweet 

# # Seccond Session: We wish to create a form that allows users to post tweets, and we want to validate the data
# # We can do this by subclassing the django.forms.Form class
# # This class provides us with a set of fields and methods that we can use to define our form
# # We start by defining the fields that we want our form to have
# # We can do this by defining class variables on our form class
# # Each class variable represents a field on our form
# # We can specify the type of field we want by setting the class variable to an instance of the field class
# # For example, we can create a field that stores a string by setting the class variable to an instance of the django.forms.CharField class
# # We can also specify the name of the field by setting the name parameter of the field class
# # We use the django.utils.translation.gettext_lazy function to specify the name of the field in a way that is compatible with django's translation system
# # We can also specify other parameters to the field class to specify other properties of the field
# # For example, we can specify the max_length parameter to the CharField class to specify the maximum length of the string that can be stored in the field

# # We can also use the django.forms.ModelForm class to create a form from a model class (see https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/)
# # We can do this by setting the model parameter of the django.forms.ModelForm class to the model class that we want to create
# # a form from by providing a meta class that specifies the fields that we want to include in the form
# # This will automatically create fields for each of the fields on the model class
# # We can also specify additional fields by defining class variables on the form class


# class TweetForm(forms.ModelForm):
#     class Meta:
#         # We specify the model that we want to create a form from
#         model = Tweet

#         # We can specify the fields that we want to include in the form by setting the fields parameter of the meta class to a list of field names
#         # We can also specify the fields that we want to exclude from the form by setting the exclude parameter of the meta class to a list of field names
#         # see https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#selecting-the-fields-to-use for more details
#         # ADDITION: chose to include "text" and "reply_to" fields by setting the fields parameter 
#         fields = [
#             # ADDITION: add text and reply_to fields 
#         ]

#         # We can specify the widgets that we want to use to render the fields on the form
#         # We can do this by defining a widgets class variable on the meta class
#         # This class variable should be a dictionary that maps the name of the field to the widget that we want to use to render the field
#         # We can use the django.forms.Textarea class to create a widget that renders a text area
#         # We can also use the django.forms.TextInput class to create a widget that renders a text input
#         # We can also use the django.forms.HiddenInput class to create a widget that renders a hidden input
#         # see https://docs.djangoproject.com/en/4.1/ref/forms/widgets/
#         # ADDITION: using forms.HiddenInput try hiding the reply_to field, and use forms.Textarea to render the text field as a text area
#         widgets = {
#             "text": forms.Textarea(attrs={"rows": 3}),
#             # ADDITION: use forms.HiddenInput to hide the reply_to field
#         }  # We use the HiddenInput widget to render the reply_to field as a hidden field in the form

#         # We can also specify the labels for the fields by providing a labels dictionary to the meta class
#         # This dictionary should map the name of the field to the label that we want to use for the field
#         # We can use the django.utils.translation.gettext_lazy function to specify the label of the field in a way that is compatible with django's translation system
#         # ADDITION: use labels to change the label of the reply_to field to "" so that it is not displayed
#         labels = {
#             # ADDITION: set the label of the reply_to field to "" so that it is not displayed
#         }

#     # It is important to note that in order to save the data from the form, we also need to have a view that
#     # adds the user that is posting the tweet to the form data
#     # we can do this by overriding the form_valid method of 
#     # the view that handles the form (see dwitter/apps/tweets/views.py)
