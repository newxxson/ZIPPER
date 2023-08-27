from .models import VerificationToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import verification_token_generator
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework import status


def create_token(user, veri_type):
    verification_token = user.verification_token

    # need to renew
    if verification_token:
        verification_token.verification_type = veri_type
        verification_token.token = verification_token_generator.make_token(user)
    else:
        token = verification_token.make_token(user)
        verification_token = VerificationToken.objects.create(
            user=user, token=token, verification_type=veri_type
        )
    return verification_token


def check_user_email(email):
    return email.lower().endswith("@korea.ac.kr")


def send_activation_email(user):
    mail_content = dict()
    mail_content["mail_subject"] = "KUZIP 이용을 위한 메일 인증"
    mail_content["request"] = "KUZIP 회원가입을 완료하기 위해서 아래 링크를 클릭해주세요!"
    mail_content["action"] = "고대 이메일 인증하기"
    send_mail(user, veri_type="EMAIL", mail_content=mail_content)


def send_password_reset_email(user):
    mail_content = dict()
    mail_content["mail_subject"] = "KUZIP 비밀번호 초기화"
    mail_content["request"] = "KUZIP 비밀번호를 잃어버리셨나요? 다음 링크를 눌러 초기화를 진행해 주세요"
    mail_content["description"] = "(만약 비밀번호 초기화 요청을 하지 않으셨다면 바로 ZIPPER팀 메일로 연락 부탁드립니다!)"
    mail_content["action"] = "비밀번호 초기화"
    send_mail(user, veri_type="PASSWORD", mail_content=mail_content)


def send_mail(user, veri_type, mail_content):
    mail_subject = mail_content["mail_subject"]
    verification_token = create_token(user, veri_type)

    message = render_to_string(
        "verification_email.html",
        {
            "username": user.username,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token": verification_token.token,
            "domain": "kuzip.kr",
            **mail_content,
        },
    )

    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    email = EmailMessage(mail_subject, message, from_email, [to_email])
    email.content_subtype = "html"
    email.send()
