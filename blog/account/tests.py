from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for account activation.
    """
    pass


account_activation_token = AccountActivationTokenGenerator()