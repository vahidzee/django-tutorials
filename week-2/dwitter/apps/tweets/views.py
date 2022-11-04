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


# @login_required(login_url=reverse_lazy("login"))
# def index(request):
#     return render(
#         request,  # the request object
#         "generic_message.html",  # <-- This is the template we want to use
#         {
#             "content": f"Welcome to Dwitter, {request.user.username}!"  # context to pass to template
#         },  # <-- We use the username of the logged in user to personalize the message
#     )

# Second Session: We want to show the user a list of the tweets of all of the users on Dwitter
# (We ignore following for simplification), and we want to allow the user to post a tweet or reply to a tweet

# To show the user a list of tweets, we just get a list of all the tweets from the database (sorted by the time they were uploaded)
# and pass it to the template to render

# To allow the user to post a tweet, we need to create a form that the user can fill out to post a tweet
# We implement the form in the tweets/forms.py file (see the comments in that file for more details)

# We then create a view that renders the form to the user, to handle replies, we just pass the id of the tweet we are replying to
# to the view, and the view will render the form with the id of the tweet we are replying to as a hidden field in the form
# The form will then be submitted to the same view, and the view will handle the form submission and create a new tweet

# We also want to make sure that only logged in users can access this view, and if a user is not logged in they should be redirected to the login page
# (We did this in our previous session, see the commented codes above)

# The index template is already implemented for you (in templates/index.html), you just need to pass the tweets and the form to the template
from django.views.generic import ListView  # We use the ListView generic view to render a list of objects
from django.views.generic.edit import FormView  # We use the FormView generic view to render a form
from .models import Tweet  # We import the Tweet model
from .forms import TweetForm  # We import the TweetForm form
from django.shortcuts import (
    get_object_or_404,
)  # We use this function to get a tweet object from the database, or return a 404 error if the tweet does not exist
# see https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/#get-object-or-404
from django.utils.decorators import method_decorator

# Same as before we can use the login_required decorator to make sure that only logged in users can access this view
# but we should decorate the class instead of the function (see https://docs.djangoproject.com/en/4.1/topics/class-based-views/intro/#decorating-the-class)
# We can do this by using the method_decorator function from django.utils.decorators
# and we should decorate the dispatch method of the class so that the decorator is applied to all the methods in the class
# ADDITION: decorate the class with the login_required decorator and redirect to the login page if the user is not logged in

class TweetsListView(ListView):
    # We specify the model we want to use to get the list of objects
    model = Tweet 

    # We render the results in the template "index.html"
    template_name = "index.html"

    # our template expects the list of tweets to be in a variable called "tweets", so we override the
    # context_object_name attribute of the ListView generic view to set the name of the variable to "tweets"
    # default value is "object_list"
    context_object_name = "tweets"

    # to sort the tweets, we set the ordering attribute to first order by uploaded_at in a descending order
    # ordering takes a list of fields to sort by, so we can sort by multiple fields
    # (e.g. ordering = ["-uploaded_at", "+id"] will sort by uploaded_at first (descending), and if there are multiple tweets with the same uploaded_at, it will sort by id (ascending))
    # see https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by for more details
    # ADDITION: order by uploaded_at in a descending order


    # not to clutter up the response, we only return a limited number of tweets in each response
    # in order to do this, we use "pagination" (see https://docs.djangoproject.com/en/4.1/topics/pagination/)
    # we use the paginate_by attribute to specify the number of tweets to return in each response
    # ADDITION: paginate by 10 tweets and see what happens


    # override queryset to filter out tweets that are replies
    def get_queryset(self):
        # ADDITION: filter out the original queryset results to only return tweets that are not replies (i.e. tweets with reply_to=None)
        return super().get_queryset() # add your codes here


class TweetCreateView(FormView):
    # we use the "generic_form.html" template to render the form
    template_name = "generic_form.html"
    # we use the TweetForm form for this view
    form_class = TweetForm
    # we want to redirect the user to the index page after they submit the form
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # we want to pass the id of the tweet we are replying to to the template (if we are replying to a tweet)
        # we get the id of the tweet we are replying to from the url (GET parameter)
        # this way we can render the id of the tweet we are replying to as a hidden field in the form
        # so that the form will be submitted with the id of the tweet we are replying to

        # ADDITION: check if the request has a "reply_to" GET parameter, and if it does, pass the value of the "reply_to" GET parameter to the template
        # as an initial value for the reply_to field in the form
        # you should set context["form"].fields["reply_to"].initial to the value of the "reply_to" GET parameter

        
        # To customize the title of the form, we pass the title to the template as a context variable
        if self.request.GET.get("reply_to"):
            context["form_header"] = "Reply to tweet"
            context["form_description"] = "post a reply to the tweet: [{}]".format(
                get_object_or_404(Tweet, id=self.request.GET.get("reply_to"))
            )
        else:
            context["form_header"] = "Post a tweet"
            context["form_description"] = "Post a tweet to Dwitter"
        return context

    # ADDITION: override the form_valid method to handle the form submission (i.e. create a new tweet)
    # form_valid gets called when the form is submitted and is valid therefore if 
    # you wish to create a new tweet on succsessful form submission you should do it here
    # In the generic form view, if the underlying form handles save() correctly,
    # it automatically gets called in form_valid, but because we are using a custom form which does not handle save() correctly,
    # (i.e. it does not save the tweet to the database, because it doesn't have the user field), we need to call save() manually in form_valid
    # see https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-editing/#formview-objects
    def form_valid(self, form):
        # we override the form_valid method to handle the form submission
        # we get the form data from the form parameter
        # we create a new tweet object using the form data
        # we set the user of the tweet to the current user
        # we save the tweet to the database
        # we redirect the user to the index page
        # ADDITION: create a new tweet object using the form data, set the user of the tweet to the current user, and 
        # save the tweet to the database and redirect the user to the index page
       
        return super().form_valid(form)
