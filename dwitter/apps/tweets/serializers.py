from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Tweet
from ..accounts.serializers import RestrictedUserSerializer


class TweetCreateSerializer(serializers.ModelSerializer):
    # we use this serializer to create a tweet
    # we don't need to include the user field in the serializer
    # because we will set the user to the current user in the view
    # we also don't need to include the uploaded_at field in the serializer
    class Meta:
        model = Tweet
        # ADDITION: add "text" and "reply_to" fields to the serializer
        fields = ("text", "reply_to")


class TweetViewSerializer(serializers.ModelSerializer):
    # we can mention other serializers to be used for specific fields
    # in this case we use the RestrictedUserSerializer for the user field (see accounts/serializers.py)
    user = RestrictedUserSerializer(read_only=True)
    # to recursively get all replies and serialize them
    # we define a serializer method field (https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield)
    # and define a function that returns the serialized replies (get_replies)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        # ADDITION: add all fields to the serializer, you can use the "__all__" shortcut and set
        # fields = "__all__"
        fields = "__all__"
        # ADDITION: make the "user" and "uploaded_at" fields read only by adding them to the "read_only_fields" list
        # by setting read_only_fields = ["user", "uploaded_at"]
        read_only_fields = ["user", "uploaded_at"]

    def get_replies(self, tweet):
        # the tweet argument would be the tweet object that is being serialized
        # we use the "tweet.replies" attribute to get all replies to the tweet
        # and then we use the TweetViewSerializer to serialize the replies
        # we use the "many=True" argument to tell the serializer that we are serializing a list of objects
        # and not a single object
        return TweetViewSerializer(tweet.replies, many=True).data
