from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from zip.models import Review
from django.contrib.auth import get_user_model
from zip.serializers import (
    ReviewSerializer,
    AreaSerializerSimple,
    HouseSerializerSimple,
)
from .models import VerificationToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from zip.models import Area, Review, House
from rest_framework.authtoken.models import Token
from rest_auth.views import LoginView
import json
from .serializers import CustomUserPatchSerializer, CustomLoginSerializer
from django.utils.http import urlsafe_base64_decode
from .tokens import verification_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_text
from .utils import (
    check_user_email,
    send_activation_email,
    send_password_reset_email,
    is_time_interval_ok,
    verify_hash,
    verify_email_code,
)
import logging

logger = logging.getLogger(__name__)


class UserConfigView(APIView):
    def post(self, request):
        User = get_user_model()
        data = request.data
        extra_fields = {
            "student_number": data.get("student_number"),
            "sex": data.get("sex"),
            "department": data.get("department"),
            "interested_areas": data.get("interested_areas"),
        }
        try:
            token = data.pop("token", None)
            if not check_user_email(data.get("email"), token):
                return Response(
                    {"message": "invalid email"}, status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(
                email=data.get("email"),
                id=data.get("id"),
                nickname=data.get("nickname"),
                password=data.get("password"),
                **extra_fields,
            )
            logging.debug("created_user")
            token = Token.objects.create(user=user)

            return Response(
                {
                    "message": "signup complete!",
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logging.debug(e, exc_info=True)
            return Response({"message": str(e)}, status=400)

    @permission_classes([IsAuthenticated])
    def patch(self, request):
        user = request.user
        data = request.data
        serializer = CustomUserPatchSerializer(user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        user.delete()


# @api_view(["POST"])
# def send_activation_email_again(request):
#     email = request.data.get("email")
#     if is_time_interval_ok(email):
#         send_activation_email(email)
#         return Response(
#             {"message": "activation email sent"},
#             status=status.HTTP_200_OK,
#         )
#     else:
#         return Response(
#             {"message": "you need to wait to send another mail"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )


@api_view(["POST"])
def activate_user(request):
    data = request.data
    email = data.get("email")
    token = data.get("token")
    if verify_email_code(email, token):
        return Response(
            {"message": "email verified", "token": token}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"message": "invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST
        )


# 초기화 요청이 들어오고 이메일로 전송
@api_view(["POST"])
def password_reset_email(request, id):
    try:
        email = request.data.get("email")
        User = get_user_model()
        user = User.objects.get(email=email)
        if not user.is_active:
            return Response(
                {"message": "activate your account first."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not is_time_interval_ok(user):
            return Response(
                {"message": "you need to wait to send another mail"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        send_password_reset_email(user)
        return Response(
            {"message": "reset email has been sent to your email"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def verify_reset_email(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    User = get_user_model()
    user = User.objects.get(id=uid)
    try:
        verification_token = VerificationToken.objects.get(user=user)
    except Exception as e:
        return Response(
            {"message": "invalid token"}, status=status.HTTP_400_BAD_REQUEST
        )
    if (
        verification_token_generator.check_token(user, token)
        and verification_token.token == token
        and verification_token.verification_type == "PASSWORD"
    ):
        return Response(
            {
                "message": "confirmation complete",
                "verification_token": verification_token.token,
            },
            status=status.HTTP_202_ACCEPTED,
        )
    else:
        return Response(
            {
                "message": "Invalid token. The token may have been expired. Check your email inbox."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
def reset_password(request):
    data = request.data
    verification_token = data.get("verification_token", None)

    User = get_user_model()
    user = User.objects.filter(verification_token__token=verification_token)
    if user.exists():
        user = user.first()
    else:
        return Response(
            {"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    password = data.get("password")

    user.set_password(password)
    user.verification_token.delete()
    Token.objects.get(user=user).delete()
    token = Token.objects.create(user=user)
    user.save()
    return Response(
        {"message": "password was reset", "token": token},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def verify_id(request, id):
    User = get_user_model()
    if User.objects.filter(id=id).exists():
        return Response({"valid": False}, status=status.HTTP_409_CONFLICT)
    else:
        return Response({"valid": True}, status=status.HTTP_200_OK)


@api_view(["GET"])
def verify_nickname(request, nickname):
    User = get_user_model()
    if User.objects.filter(nickname=nickname).exists():
        return Response({"valid": False}, status=status.HTTP_409_CONFLICT)
    else:
        return Response({"valid": True}, status=status.HTTP_200_OK)


@api_view(["GET"])
def verify_email(request, email):
    User = get_user_model()
    if User.objects.filter(email=email).exists():
        return Response({"valid": False}, status=status.HTTP_409_CONFLICT)
    if is_time_interval_ok(email):
        send_activation_email(email)
        return Response({"message": "activation email sent"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "you need to wait to send another mail"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            if "area_code" in data:
                area_code = data.get("area_code")
                area = Area.objects.filter(area_code__in=area_code)
                state = f"retrieved area_code with {len(area)}"
                user.interested_areas.set(area)
                user.save()
            elif "house_pk" in data:
                house_pk = data.get("house_pk")
                house = House.objects.get(pk=house_pk)
                state = "retrieved house_pk"
                if user.interested_houses.exists():
                    user.interested_houses.add(house)
                else:
                    user.interested_houses.set([house])
                house.interest_num += 1
                house.save()
                user.save()
            else:
                return Response(
                    {"message": "Invalid query parameter value"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"message": "interest saved"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": str(e), "state": state},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, type):
        user = request.user
        if type == "area":
            # 관심있는 그 지역 자체만 찾기
            if request.query_params.get("simple", None):
                interested_areas = user.interested_areas.all()
                serializer = AreaSerializerSimple(interested_areas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # 관심있는 지역의 집들 리턴하기
            interested_houses = House.objects.filter(
                area__in=user.interested_areas.all()
            )
            serializer = HouseSerializerSimple(
                interested_houses, many=True, context={"request": request}
            )
        elif type == "house":
            interested_houses = user.interested_houses.all()
            serializer = HouseSerializerSimple(
                interested_houses, many=True, context={"request": request}
            )
        else:
            return Response(
                {"message": "Invalid query parameter value"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, type, pk):
        user = request.user
        if type == "area":
            area = Area.objects.get(area_code=pk)
            user.interested_areas.remove(area)
            user.save()

        elif type == "house":
            house = House.objects.get(pk=pk)
            user.interested_houses.remove(house)
            house.interest_num -= 1
            house.save()
            user.save()
        else:
            return Response(
                {"message": "Invalid query parameter value"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "delete successful"}, status=status.HTTP_204_NO_CONTENT
        )


# retreive user written reviews
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_review(request):
    user = request.user

    review = user.reviews.all()
    serializer = ReviewSerializer(review, many=True, context={"user": request.user})
    return Response(serializer.data, status=status.HTTP_200_OK)


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
