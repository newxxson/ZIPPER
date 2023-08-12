from .models import EmailActivationToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import get_user_model


def create_email_token(user):
    token = account_activation_token.make_token(user)
    activation_token = EmailActivationToken.objects.create(user=user, token=token)

    return activation_token


def check_user_email(email):
    return email.lower().endswith("@korea.ac.kr")
