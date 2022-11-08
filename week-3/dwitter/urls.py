"""dwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include  # ADDITION
from dwitter.apps.accounts import views as accounts_views  # ADDITION
from dwitter.apps.tweets import views as tweets_views  # ADDITION

# we can use the include function to include the urls from another app
# we connect the urls from django's authentication system to our app by including the urls from django.contrib.auth.urls
# by adding:
#     path("accounts/", include("django.contrib.auth.urls")),
# all the urls from django auth system will be available at /accounts/ (so for example the login page will be at /accounts/login/)
# see https://docs.djangoproject.com/en/4.1/topics/auth/default/#module-django.contrib.auth.views for more info

# we connect the signup view to the /accounts/signup/ url by adding:
#     path("accounts/signup/", accounts_views.signup, name="signup"),
# by naming the url "signup", we can use {% url "signup" %} in our templates to get the url for the signup page (see templates/regiration/login.html)

# we connect the index view to the root url by adding:
#     path("", tweets_views.index, name="index"),

# we connect the admin view to the /admin/ url by adding:
#     path("admin/", admin.site.urls),
# admin configurations are definend in dwitter/apps/*/admin.py files

# Session 3: adding a base router for the APIs and connecting APIs to our django app urls (at /api/)
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
# we can use the DefaultRouter to create a default router that will register all our viewsets with it
# see https://www.django-rest-framework.org/api-guide/routers/#defaultrouter for more info
#
router = routers.DefaultRouter()
router.get_api_root_view().cls.__name__ = (
    "Dwitter API"  # customize the name of the root view (shown in the browsable API)
)
router.get_api_root_view().cls.__doc__ = "Fully browsable API for the Dwitter project."  # customize the description of the root view (shown in the browsable API)

# ADDITION: connect the rest viewsets to the router using router.register
router.register("accounts", accounts_views.AccountsAPIViewSet, basename="accounts")
router.register("tweets", tweets_views.TweetsAPIViewSet, basename="tweets")

urlpatterns = [
    path("admin/", admin.site.urls),
    # user urls
    path("accounts/", include("django.contrib.auth.urls")),  # ADDITION: include the default auth urls
    path("accounts/signup/", accounts_views.SingUpFormView.as_view(), name="signup"),  # ADDITION: add the signup url
    # tweet urls
    path("", tweets_views.TweetsListView.as_view(), name="index"),  # ADDITION: add the index url
    path("tweet/", tweets_views.TweetCreateView.as_view(), name="tweet"),  # ADDITION: add the tweet url
    # rest framework urls
    path(
        "api/auth/", include("rest_framework.urls", namespace="rest_framework")
    ),  # ADDITION: include the rest framework urls (e.g.: for session auth in browsable api)
    # api urls
    path("api/", include(router.urls)),  # ADDITION: include the api urls
]
