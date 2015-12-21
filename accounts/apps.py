from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """ App configuration for accounts app.
    """

    name = 'accounts'

    def ready(self):
        import accounts.signals.accounts
