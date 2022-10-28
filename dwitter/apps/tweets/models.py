from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Session 2: We wish to create a model to store the tweets that users post on Dwitter
# We can do this by subclassing the django.db.models.Model class
# This class provides us with a set of fields and methods that we can use to define our model

# We start by defining the fields that we want our model to have
# We can do this by defining class variables on our model class
# Each class variable represents a field on our model
# We can specify the type of field we want by setting the class variable to an instance of the field class
# For example, we can create a field that stores a string by setting the class variable to an instance of the django.db.models.CharField class
# We can also specify the name of the field by setting the name parameter of the field class
# We use the django.utils.translation.gettext_lazy function to specify the name of the field in a way that is compatible with django's translation system
# We can also specify other parameters to the field class to specify other properties of the field
# For example, we can specify the max_length parameter to the CharField class to specify the maximum length of the string that can be stored in the field


class Tweet(models.Model):
    # The user who posted the tweet (see https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey)
    # We use the django.contrib.auth.get_user_model function to get the user model that is currently in use
    # We do this because the user model can be swapped out by the user of the application (see https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model)
    # We use the on_delete parameter to specify what should happen to the tweet if the user is deleted
    # We set it to CASCADE so that if the user is deleted, the tweet is also deleted
    # We also set the related_name parameter to "tweets" so that we can access the tweets posted by a user using the tweets attribute of the user object
    # For example, we can get the tweets posted by the user with id 1 using the following code:
    #   user = User.objects.get(id=1)
    #   tweets = user.tweets.all()
    # ADDITION: create a user field that stores the user who posted the tweet
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="tweets")

    # The text of the tweet (see https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.CharField)
    # We set the max_length parameter to 280 because that is the maximum length of a tweet (see https://help.twitter.com/en/using-twitter/twitter-character-limits)
    # ADDITION: create a reply_to field that stores the tweet that this tweet is a reply to (see https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey)
    # you should create a foreign key to the Tweet model!, set the related_name parameter to "replies", and set the on_delete parameter to CASCADE, so that if the tweet that this tweet is a reply to is deleted, this tweet is also deleted
    # this field should be nullable, so that we can create tweets that are not replies to other tweets
    reply_to = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
    )

    # ADDITION: create a text field that stores the text of the tweet (with a max length of 280)
    text = models.CharField(_("Text"), max_length=280, blank=False)
    
    # ADDITION: use the django.db.models.DateTimeField class to create an uploaded_at field that stores the time that the tweet was uploaded
    # you should set the auto_now_add parameter to True so that the time is automatically set to the current time when the tweet is created
    uploaded_at = models.DateTimeField(auto_now=True)

    # create a __str__ method to return the text of the tweet (and username and upload time) when we print the tweet object (see https://docs.djangoproject.com/en/4.1/ref/models/instances/#str)
    # this is useful in django admin and in other places where we want to display the tweet object
    def __str__(self):
        return f"{self.user.username} at {self.uploaded_at}: {self.text}"
