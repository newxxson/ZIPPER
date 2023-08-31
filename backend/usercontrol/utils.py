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
from django.utils import timezone
import datetime
import random
import time
import hashlib


def create_hash(email):
    current_time = str(int(time.time()))  # Current time in seconds
    combined_string = f"{email}{current_time}"
    hash_value = hashlib.sha256(combined_string.encode()).hexdigest()
    return hash_value, current_time


def verify_hash(email, hash_value, timestamp, interval=5):
    current_time = int(time.time())
    if current_time - int(timestamp) > interval:
        return False, "Time interval exceeded"

    combined_string = f"{email}{timestamp}"
    verify_hash = hashlib.sha256(combined_string.encode()).hexdigest()

    if verify_hash == hash_value:
        return True
    else:
        return False


def create_token(email, veri_type):
    verification_token = VerificationToken.objects.filter(email=email)

    # need to renew
    if verification_token.exists():
        verification_token = verification_token.first()
        verification_token.verification_type = veri_type
        if veri_type == "EMAIL":
            verification_token.token = random.randint(100000, 999999)
            verification_token.timestamp = time.time()
        elif veri_type == "PASSWORD":
            verification_token.token, verification_token.timestamp = create_hash(email)
        verification_token.used += 1
    else:
        if veri_type == "EMAIL":
            token = random.randint(100000, 999999)
            timestamp = time.time()
        elif veri_type:
            token, timestamp = create_hash(email)
        verification_token = VerificationToken.objects.create(
            email=email, token=token, verification_type=veri_type, timestamp=timestamp
        )
    return verification_token


def check_user_email(email, token):
    verification_token = VerificationToken.objects.filter(email=email)
    if not verification_token.exists():
        return False
    verification_token = verification_token.first()

    if verification_token.token != token:
        return False
    else:
        verification_token.delete()
        return True


def send_mail(user, veri_type, mail_content):
    mail_subject = mail_content["mail_subject"]
    to_email = user if veri_type == "EMAIL" else user.email
    verification_token = create_token(to_email, veri_type)

    if veri_type == "PASSWORD":
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
    elif veri_type == "EMAIL":
        message = render_to_string(
            "activation_email.html", {"token": verification_token.token, **mail_content}
        )

    from_email = settings.EMAIL_HOST_USER
    email = EmailMessage(mail_subject, message, from_email, [to_email])
    email.content_subtype = "html"
    email.send()


def send_activation_email(email):
    mail_content = dict()
    mail_content["mail_subject"] = "KUZIP 이용을 위한 메일 인증"
    mail_content["request"] = "KUZIP 회원가입을 완료하기 위해서 아래 링크를 클릭해주세요!"
    mail_content[
        "description"
    ] = "(만약 ZIP 회원가입을 진행하지 않으셨다면 바로 koreaunivzipper@outlook.com으로 연락부탁드립니다.)"
    send_mail(email, veri_type="EMAIL", mail_content=mail_content)


def send_password_reset_email(user):
    mail_content = dict()
    mail_content["mail_subject"] = "KUZIP 비밀번호 초기화"
    mail_content["request"] = "KUZIP 비밀번호를 잃어버리셨나요? 다음 링크를 눌러 초기화를 진행해 주세요"
    mail_content["description"] = "(만약 비밀번호 초기화 요청을 하지 않으셨다면 바로 ZIPPER팀 메일로 연락 부탁드립니다!)"
    mail_content["action"] = "비밀번호 초기화"
    mail_content["request_type"] = "reset"
    send_mail(user, veri_type="PASSWORD", mail_content=mail_content)


def verify_email_code(email, token):
    verification_token = VerificationToken.objects.filter(email=email)
    if not verification_token.exists():
        return False
    verification_token = verification_token.first()
    if verification_token.token != token or (
        time.time() - verification_token.timestamp > 5 * 60
    ):
        return False
    else:
        return True


def is_time_interval_ok(email):
    verification_token = VerificationToken.objects.filter(email=email)
    if not verification_token.exists():
        return True
    verification_token = verification_token.first()
    if (
        time.time() - verification_token.timestamp < 5 * 60
    ) and verification_token.used > 1:
        return False
    else:
        return True
