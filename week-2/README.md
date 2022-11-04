# Django Tutorials CSC309 - Week 2

Our focus this week is on django models, migrations, admin, and views.
We intend to add a Tweet model to our project, and add a view to display a list of tweets and also a view to create new tweets. 
You can imagine that the front-end team for your project has already created the templates for these views, and you can find them in the `templates` directory (`index.html` and `tweet.html`).

During the meetings with tweeter clients and engineers, we have decided apon the following data model for our tweets:

* A tweet has a `text` field, which is a string of at most 280 characters.
* A tweet has a `uploaded_at` field, which is a datetime field containing the time at which the tweet was uploaded.
* A tweet has a `user` field, which is the author of the tweet.
* A tweet has a `reply_to` field, which specifies which tweet this tweet is a reply to. This field is optional, and can be null.

## Part 0: Setup

After cloning the repository, make sure you have everything setup properly (see [previous week's README](./Session-1.md) for instructions). Make sure you have everything installed `pip install -r requirements.txt` and that you are able to run the development server `python manage.py runserver`. 

If you are cloning the codes and not just applying the changes to the previous session's codes, you will need to create a new database (apply migrations) `python manage.py migrate`. (see [previous week's README](../week-1//README.md) for instructions).

Our apps are already setup in our `settings.py` file, so we don't need to do anything there. We will be working in the `tweets` app, so make sure you are in the `tweets` directory. (We don't bother working with URLs in this tutorial, we did that last week).

## Part 1: Creating the Tweet Model

Let's start by creating our Tweet model in `tweets/models.py`. You can follow the comments in this file to create the model.

After you have created the model, you need to create a migration for it. Run `python manage.py makemigrations tweets` to create the migration file. You can then run `python manage.py migrate` to apply the migration to your database. (If you run into any issues, you can comment out other boilerplate codes in `admin.py` and `views.py` to get rid of any errors).

## Part 2: Creating the Tweet Admin

Now that we have a Tweet model, we want to be able to create tweets from the admin page. We can do this by creating a TweetAdmin class in `tweets/admin.py`. You can follow the comments in this file to create the admin class.

After you are finished implementing the requirements layed in the comments, you can run `python manage.py runserver` to start the development server. You can then go to `http://localhost:8000/admin` to access the admin page. 

In order to access the admin page, you need to create a superuser. You can do this by running `python manage.py createsuperuser` and following the instructions. You can then login to the admin page using the credentials you just created (see [this link](https://docs.djangoproject.com/en/4.1/intro/tutorial02/#introducing-the-django-admin) for more information).

After loging into the admin page you should be able to see the Tweet model in the admin page, and you should be able to create new tweets, look up tweets (by tweets' content texts or auther usernames), and see details of tweets (including inline forms to create replies).

Test out the admin page to make sure everything is working properly.

## Part 3: Creating the Tweet View

Now that we have a Tweet model and an admin page, we want to be able to display a list of tweets and also create new tweets. We can do this by creating a TweetView class in `tweets/views.py`. You can follow the comments in this file to create the view class.

After you are finished implementing the requirements layed in the comments, you can run `python manage.py runserver` to start the development server. You can then go to `http://localhost:8000/` to access the index page.

## Part 4: Tweet creation form

The only thing left to do is to create a view which lets us create new tweets (which could be replies to other tweets). We can do this by creating a TweetCreateView class in `tweets/views.py` based on the form that you will implement in `tweets/forms.py` called TweetForm. You can follow the comments in these files to create the view class.

After you are finished implementing the requirements layed in the comments, you can run `python manage.py runserver` to start the development server. You can then go to `http://localhost:8000/tweet` to access the tweet creation page. You should be able to create new tweets and replies to existing tweets. (To create a reply, you need to specify the id of the tweet you are replying to in the URL as a GET parameter called `reply_to`, see [this](https://www.semrush.com/blog/url-parameters/) for more details).

Go back to the main page and make sure that you can see the tweets you just created. Try creating a reply to a tweet and make sure that you can see the reply on the main page as well. You can also cross check with the admin page to make sure that the tweets you created are there as well.

Good job! You have completed the second week of the Django tutorial. Have fun django-ing!
