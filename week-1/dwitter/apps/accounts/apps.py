from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dwitter.apps.accounts' # This is the important line that tells Django where to find the app
    # it should follow the format of the project structure
