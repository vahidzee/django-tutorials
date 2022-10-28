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
