from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from zip.models import Review
from django.contrib.auth import get_user_model
from zip.serializers import (
    ReviewSerializer,
    HouseSerializer,
    AreaSerializer,
    HouseSerializerSimple,
)
from .models import EmailActivationToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from zip.models import Area, Review, House
from rest_framework.authtoken.models import Token
from rest_auth.views import LoginView
import json
from .serializers import CustomUserPatchSerializer, CustomLoginSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .utils import check_user_email, create_email_token
from django.conf import settings


class UserConfigView(APIView):
    def post(self, request):
        User = get_user_model()
        data = request.data
        extra_fields = {
            "age": data.get("age"),
            "sex": data.get("sex"),
            "department": data.get("major"),
            "interested_areas": data.get("interested_areas"),
        }
        try:
            if not check_user_email(data.get("email")):
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

            current_site = get_current_site(request)
            mail_subject = "Activate your blog account."

            activate_token = create_email_token(user)

            message = render_to_string(
                "acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),
                    "token": activate_token.token,
                },
            )
            from_email = settings.EMAIL_HOST_USER
            to_email = data.get("email")
            email = EmailMessage(mail_subject, message, from_email, [to_email])
            email.content_subtype = "html"
            email.send()

            return Response(
                {"message": "confirmation email was sent to your email account"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
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


@api_view(["GET"])
def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(id=uid)
        if user.is_active:
            return Response(
                {"message": "already confirmed"}, status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        user = None
        return Response(
            {"message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        activate_token = EmailActivationToken.objects.get(user=user)
    except:
        return Response(
            {"message": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )
    if user is not None and token == activate_token.token:
        user.is_active = True
        activate_token.delete()
        user.save()
        token = Token.objects.create(user=user)
        # return redirect('home')
        print(token)
        return Response(
            {"message": "confirmation complete", "token": token.key},
            status=status.HTTP_202_ACCEPTED,
        )
    else:
        return Response(
            {"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
def verify_id(request, id):
    user = get_user_model()
    if user.objects.filter(id=id).exists():
        return Response({"valid": False}, status=status.HTTP_409_CONFLICT)
    else:
        return Response({"valid": True}, status=status.HTTP_200_OK)


@api_view(["GET"])
def verify_nickname(request, nickname):
    user = get_user_model()
    if user.objects.filter(nickname=nickname).exists():
        return Response({"valid": False}, status=status.HTTP_409_CONFLICT)
    else:
        return Response({"valid": True}, status=status.HTTP_200_OK)


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
                    user.interested_houses.set(house)
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
