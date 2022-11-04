# Django Tutorials CSC309 - Week 3

Our goal for this week is to add  [REST API](https://en.wikipedia.org/wiki/Representational_state_transfer)s to our project for the following user stories using the [`django-rest-framework`](https://www.django-rest-framework.org/):

- authentication (login, logout, register)
- tweets (create, list[index page])

## Virtual Enviroment
As you have probably noticed by now, when developing python projects, it is common to use virtual environments. This is a way to isolate your project dependencies from the rest of your system. This is especially important when working on multiple projects that have conflicting dependencies (e.g. different versions of the same library).
Another benefit of using virtual environments is that you can easily share your project with others without worrying about them having to install all the dependencies on their own.

It is recommended that you use `virtualenv` to create your virtual environments. You can install it using `pip`: `pip install virtualenv`

To create a virtual environment, run the following command in the root of your project:

```bash
virtualenv venv
```

This will create a folder called `venv` in your project directory. This folder contains all the dependencies for your project. To activate the virtual environment, run the following command:

```bash
source venv/bin/activate
```

To deactivate the virtual environment, run the following command:

```bash
deactivate
```

Once you have a virtual environment activated, both `pip` and `python` will use the dependencies in the virtual environment. This means that you can install dependencies for your project without affecting the rest of your system.
This also means that it is possible to have multiple versions of Python installed on your system and use different versions for different projects (using different python-venvs).

To handle different versions of Python, you can use `pyenv` to install and manage different versions of Python. Pyenv is a tool that allows you to easily switch between multiple versions of Python. It also has a virtual environment plugin that allows you to create virtual environments for different versions of Python, and lets you automate the process of creating virtual environments for different versions of Python. See [this](https://realpython.com/intro-to-pyenv/) for more information on pyenv, and its installation.

If you are a Mac user, I duely recommend reading [this](https://faun.pub/the-right-way-to-set-up-python-on-your-mac-e923ffe8cf8e) article on how to properly set up Python and virtual environments on your Mac.

## Part 0: Setup
As usual, clone this repo, or apply the changes to your copy by pulling/applying the changes. To practice using virtual environments, create a new virtual environment for this project. And install the dependencies using your virtual enviroment's `pip`: `pip install -r requirements.txt`. This will install the following dependencies in your virtual environment: (1) django, (2) djangorestframework, (3) django-widget-tweaks (which we used to prettify our forms templates in week 1).

It's important to note that, as before if you are not continuing from week 2, you have to create the database (create and apply the migrations), so in that case run the following commands:

```bash
python manage.py makemigrations tweets
python manage.py migrate
```

## Part 1: Adding the `rest_framework` app
To add the `rest_framework` app to our project, we need to add it to the `INSTALLED_APPS` in our `settings.py` file. Add `''rest_framework'` to the list of installed apps.

Django rest offers a lot of functionality out of the box, to see what it offers, check out the [documentation](https://www.django-rest-framework.org/). 

To have an idea of what is going on, `django-rest` provides a set of views (which respond to HTTP requests with JSON data/ any other form of data serialization). It also provides handy webbrowsable interfaces for such views. 
`django-rest` expect us to define how the data should be serialized (which is usually done by defining serializers, see [this](https://www.django-rest-framework.org/api-guide/serializers/) for more details). It uses serializers to convert data to and from [JSON](https://en.wikipedia.org/wiki/JSON) (or any other form of data parsing). 

It is highly recommended that you read django-rest's [official tutorials](https://www.django-rest-framework.org/tutorial/quickstart/) to get a better understanding of how it works, skim through these articles before moving on to the next part:
- [Serialization](https://www.django-rest-framework.org/tutorial/1-serialization/)
- [Requests and Responses](https://www.django-rest-framework.org/tutorial/2-requests-and-responses/)
- [Class-based Views](https://www.django-rest-framework.org/tutorial/3-class-based-views/)
- [Authentication and Permissions](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)
- [Relationships and Hyperlinked APIs](https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/)
- [ViewSets & Routers](https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/)

In order to have a webbrowsable interface (that also handles authentication using sessions), we need to add a router to our project. Look at the `urls.py` file to see how we have added the router to our project. The router is in charge of managing the urls for our API. It also provides a webbrowsable interface for our API.
See [this](https://www.django-rest-framework.org/api-guide/routers/) for more details on routers.

Most of the codes and comments following this section are self explanatory, but make sure to read the comments and the documentation to understand what is going on.

## Part 2: Authentication APIs
We will start by adding the authentication APIs. django-rest provides various authentication policies out of the box, including `BasicAuthentication`, `SessionAuthentication`, `TokenAuthentication`, and `OAuth1Authentication`. We will use `TokenAuthentication` for our project (which is the most common authentication method used in REST APIs). (See [this](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) for more details on `TokenAuthentication`).

This authentication method is based on the use of tokens. Tokens are generated by the server and sent to the client. The client then sends the token to the server with each request. The server then verifies the token and returns the requested data. This is a very common authentication method used in REST APIs. 

To use `TokenAuthentication`, we need to add it to the `DEFAULT_AUTHENTICATION_CLASSES` in our `settings.py` file. Add `rest_framework.authentication.TokenAuthentication` to the list of authentication classes, and `rest_framework.authtoken` to the list of installed apps. see [this](https://www.django-rest-framework.org/api-guide/authentication/#setting-the-authentication-scheme) for more details on how to set the authentication scheme. It's already implemented in the `settings.py` file in this repo so you don't have to do anything. If you are adding django-rest to a pre-existing project, you will have to apply migrations (to create TOKEN databases) as well. After connecting everything, you should also be able to see TOKENS in the admin panel.

Now we want to create the API endpoints for our authentication (login/logout/register). For loging in we need to recieve user credentials (username and password) and return a token. For logging out we need to recieve a token and delete it (if it exists). For registering we need to recieve user credentials (username and password) in addition to user information and create a new user. 
To handle these data transactions between the client and the server, we need to define serializers.

### Serializers
In `dwitter/apps/accounts/serializers.py`, go through the serializers, try to implement the blank pieces, until you have all three serializers implemented.

For loging in we don't need to define a serializer, we can use the `rest_framework.authtoken.serializers.AuthTokenSerializer` serializer. This stock serializer provides us with all the functionality we need to implement the login API. We just need to add it to our `accounts/views.py` file later.

Now that we have all the serializers implemented, we can move on to the permissions.

### Permissions
Django Rest provides a set of permissions classes that we can use to control who can access our API endpoints. We will use the `IsAuthenticated` permission class to control access to our API endpoints. This permission class will allow access only to authenticated users. (See [this](https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated) for more details on `IsAuthenticated`). We will also use the `AllowAny` permission class to allow access to all users. (See [this](https://www.django-rest-framework.org/api-guide/permissions/#allowany) for more details on `AllowAny`).

In `dwitter/apps/accounts/permissions.py`, go through the permissions, try to implement the blank pieces, until you have both permissions implemented. There we implement a custom permission class that only allows the user to access their own data, if they are not an admin (this permission should be applied on top of the `IsAuthenticated` permission).

### Views
In `dwitter/apps/accounts/views.py`, go through the views, try to implement the blank pieces. After you have implemented all the views, you should be able to test the API endpoints for accounts using the webbrowsable interface.

## Part 3: Tweet APIs
Similar to implementing the authentication APIs, we need to implement three types of logic for the tweet APIs:

- Create the serializers for the tweet model (view and create tweets) in `dwitter/apps/tweets/serializers.py`.
- Create the permissions for the tweet model (access relavant data only) in `dwitter/apps/tweets/permissions.py`.
- Create the views for the tweet model (view and create tweets) in `dwitter/apps/tweets/views.py`.

After you have implemented all the views, you should be able to test the API endpoints for tweets using the webbrowsable interface.

Good job! You have successfully implemented a dummy twitter project using django and django-rest. 
Have fun Djangoing!







