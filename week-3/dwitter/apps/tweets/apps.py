from django.apps import AppConfig


class TweetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dwitter.apps.tweets' # <-- This is the important line
    # If you wish to change the project structure like I did to 
    # have your apps all in a single folder, you have to manually change this
    
