from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .forms import SignupForm


class SignupSerializer(serializers.ModelSerializer):
    # just like django ModelForm, we can use a ModelSerializer to create a serializer for a model
    # we chose the fields we want to include in the serializer in the Meta class (if they are included in the model)
    # and we can add extra fields that are not included in the model as class attributes of the serializer
    # for example to have a signup form that asks for the user's username, firstname, lastname, email, and password
    # we would also like to have an additional field to confirm the password (password2)

    # ADDITION: add a password2 field to the serializer using serializers.CharField
    # set it to be required, and set its write_only attribute to True, and set its style attribute to {'input_type': 'password'}
    # this will make it a password field in the browsable api
    password2 = serializers.CharField(label=_("Confirm password"), write_only=True, style={"input_type": "password"})

    class Meta:
        model = get_user_model()  # returns the User model that is active in this project
        fields = ("username", "password", "password2", "first_name", "last_name", "email")

        # just like in django forms, we can specify the type of input to use for a field using the style attribute
        # we can also specify the write_only attribute to specify that a field should only be used for writing data
        # and not for reading data
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def validate(self, data: dict) -> dict:
        # we can override the validate method to add custom validation logic
        # we can pass this dictionary to the SignupForm class
        # ADDITION: pass the data to the SignupForm class and call its is_valid method
        data["password1"] = data["password"]
        form = SignupForm(data=data)
        # we can then call the is_valid method of the form to validate the data
        # this will validate the data and return True if the data is valid
        # and False if the data is invalid
        if form.is_valid():
            # if the data is valid, we can return the data
            return data
        else:
            # if the data is invalid, we can raise a serializers.ValidationError
            # we can pass the errors from the form to the ValidationError
            # this will make the errors from the form available in the browsable api
            raise serializers.ValidationError(form.errors)

    def create(self, validated_data: dict) -> get_user_model():
        # we can override the create method to add custom logic for creating the user
        # we can pass the validated data to the SignupForm class
        # ADDITION: pass the validated data to the SignupForm class and call its save method
        data = validated_data.copy()
        data["password1"] = data["password"]
        form = SignupForm(data=data)
        # we can then call the save method of the form to create the user
        # this will create the user and return the user
        user = form.save(commit=False)
        return user

    def save(self, **kwargs):
        # we can override the save method to add custom logic for saving the user
        # we can call the create method of the serializer to create the user
        # ADDITION: call the create method of the serializer to create the user
        user = self.create(self.validated_data)
        # we can then call the save method of the user to save the user
        # this will save the user and return the user
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # we use this serializer to serialize the user model in the browsable api (get its data and display it/allow editing it)
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]
        read_only_fields = ["password"]  # we can also specify a list of fields to be read only (not editable)


class RestrictedUserSerializer(serializers.ModelSerializer):
    # we use this serializer to just show general information about a user (username, first_name, last_name, and email) (not editable)
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]
        read_only_fields = ["username", "first_name", "last_name", "email"]
