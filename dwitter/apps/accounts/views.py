from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import SignupForm
from django.urls import reverse_lazy

# We wish to create a signup view that shows a signup form upon GET requests and
# recieves a POST request with the user data and after validating the data, creates a new user
# and redirects the user to the login page
# We can do this by manually creating a view (functional/Class based) to show a hardcoded HTML form
# and then manually reading the data from the POST request and validating it and creating a new user
# but in addition to this being a lot of work, it is also error prone and not very maintainable
# To handle data inputs from users, django introduces the concept of forms
# Forms are a way to define the fields that you want to ask from the user and the logic to validate the data
# Forms are usually defined in a forms.py file in the app folder (see dwitter/apps/accounts/forms.py for the SignupForm)

# Now that we have a form, we just need to show it to the user and handle the POST request
# We can do this by using the FormView class from django.views.generic.edit (see https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-editing/#formview)
# This class provides a way to show a form to the user and handle the POST request
# We just need to subclass this class and define the form_class attribute to be our SignupForm
# and set the template_name attribute to be the template we want to use to show the form
# and define the get_success_url method to return the url to redirect the user to after the form is successfully submitted
# and we are done

# For the success_url, we can use the reverse_lazy function from django.urls to look up the view name we want to redirect to
# in this case, we want to redirect to the login page, so we can use the name of the login view (`login`) and pass it to the reverse_lazy function
# reverse_lazy is similar to reverse, but it is lazy and can be used in places where reverse cannot be used
# (https://stackoverflow.com/questions/48669514/difference-between-reverse-and-reverse-lazy-in-django)
# To see where the login view is defined, see https://docs.djangoproject.com/en/4.1/topics/auth/default/#module-django.contrib.auth.views
# As a reminder, we connected the login view to our project in the urls.py file (see dwitter/urls.py), by
# adding the following line:
#   path('accounts/', include('dwitter.apps.accounts.urls')),
# which means that the login view is available at the url `/accounts/login/`
# So the reverse_lazy function will return the url `/accounts/login/` when we pass it the name of the login view (`login`)
# and we can use this url to redirect the user to the login page after the signup form is successfully submitted

# For the template, we can either create a new template or use an existing one
# Becacuse we are using the FormView, a form and action object will be passed to the template, therefore
# the generic_form.html which rendered forms off of these context variables will work for us


class SingUpFormView(FormView):
    # these class attributes are required by the FormView class (and automatcally handled by it)
    template_name = "generic_form.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

    def render_to_response(
        self, context, **response_kwargs
    ):  # this function is called when the view is called with a GET request
        # we can override this method to add- some extra context
        # our generic_form.html template looks for the "form_header" variable
        # and if present, it will render it as the header of the form
        # therefore to have a better looking form, and not just a generic render of the form fields
        # we can add a header to the form
        context = self.get_context_data(**context)  # get the context data from the form view
        context["form_header"] = "Create an account!"
        return FormView.render_to_response(
            self, context, **response_kwargs
        )  # render the template with the updated context

    # ADDITION: save the user to the database (see dwitter/apps/accounts/forms.py for the save method)
    # you just need to call the save method on the form object with the commit=True argument
    def form_valid(self, form):
        # form_valid function is called when the view is called with a POST request and the form is valid
        # we can override this method to do some extra logic (e.g. saving the form to the database)

        # in this case, we want to create a new user using the data from the form
        # and then redirect the user to the login page (which we defined in the success_url attribute,
        # and is handled by the FormView.form_valid method), so we just need to call the save method
        # on the form object with the commit=True argument
        user = form.save(commit=True)
        # we then call the form_valid method of the FormView class to handle the rest (redirecting the user)
        return super().form_valid(form)


# Session 3: Addin Accounts APIs with Django REST Framework
import rest_framework
from rest_framework import viewsets as drf_viewsets
from rest_framework import mixins as drf_mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from . import serializers, permissions
import django
from django.contrib.auth import get_user_model


class AccountsAPIViewSet(
    drf_viewsets.GenericViewSet,
    drf_mixins.CreateModelMixin,  # for model creation (signup)
    drf_mixins.RetrieveModelMixin,  # for model retrieval (profile)
    drf_mixins.UpdateModelMixin,  # for model update (profile update)
):
    # the docstring is used to generate the documentation for the API
    """
    API for user information management and retrieval

    * **Login** [ [login](/api/accounts/login/) | `POST` ]: obtain a valid authentication token by sending valid credentials
    * **Logout** [ [logout](/api/accounts/logout/) | `POST`]: invalidate currently owned authentication token
    * **Retrieve User** [ `<username>` | `GET`, `PUT` ]: obtain user information (by looking up username) or update user information
    """

    lookup_field = "username"  # the field to use to look up the user (in this case, the username)
    lookup_url_kwarg = "username"  # the url parameter to use to look up the user (in this case, the username)
    authentication_classes = [
        rest_framework.authentication.SessionAuthentication,
        rest_framework.authentication.TokenAuthentication,
    ]  # the authentication classes to use for this viewset

    queryset = get_user_model().objects.all()  # the queryset to use to look up the user

    # the following function is used to get the serializer class to use for the view
    # we override it to use different serializers for different rest_framework.decorators.actions
    def get_serializer_class(self):
        if self.action == "create":  # if the action is create (signup)
            return serializers.SignupSerializer
        if self.action in ["retrieve", "update"]:
            if self.request.user.is_staff or (
                "username" in self.request.parser_context["kwargs"]  # if retrieving/updating a specific user
                and self.request.user.username == self.request.parser_context["kwargs"]["username"]
            ):
                # if the user is staff or the user is looking up their own profile
                # they should be able to see and edit everything
                return serializers.UserSerializer
            else:
                # otherwise, they should only be able to see and edit their own profile
                return serializers.RestrictedUserSerializer
        elif self.action == "login":
            return AuthTokenSerializer
        elif self.action == "logout":
            # we don't need a serializer for the logout action
            # (we just need to invalidate the token, and send a success response)
            # so it suffices to return a dummy serializer (base django rest framework serializer)
            return rest_framework.serializers.Serializer
        return serializers.UserSerializer

    # we override this function to use different permissions for different actions
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["create", "login"]:
            # if the action is create (signup) or login (obtain token) then we don't need any permissions
            permission_list = [rest_framework.permissions.AllowAny]
        elif self.action in ["update", "partial_update"]:  # if the action is update/partial_update (profile update)
            permission_list = [permissions.IsSelfOrAdmin, rest_framework.permissions.IsAuthenticated]
        elif self.action in ["retrieve", "logout"]:
            permission_list = [rest_framework.permissions.IsAuthenticated]
        else:
            permission_list = [rest_framework.permissions.AllowAny]
        return [permission() for permission in permission_list]

    @rest_framework.decorators.action(methods=["POST"], detail=False)
    def login(self, request, format=None):
        """
        Obtain an authentication token by providing valid credentials.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = rest_framework.authtoken.models.Token.objects.get_or_create(user=user)
        return rest_framework.response.Response({"token": token.key})

    @rest_framework.decorators.action(methods=["POST"], detail=False)
    def logout(self, request, format=None):
        """
        Invalidate the currently owned authentication token.

        **Permissions** :

        * _Authentication_ is required
        """
        django.shortcuts.get_object_or_404(rest_framework.authtoken.models.Token, user=request.user).delete()
        return rest_framework.response.Response(status=rest_framework.status.HTTP_202_ACCEPTED)
