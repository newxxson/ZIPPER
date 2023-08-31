# users/urls.py
from django.urls import include, path
from .views import (
    UserConfigView,
    CustomLoginView,
    verify_id,
    verify_nickname,
    activate_user,
    send_activation_email,
    password_reset_email,
    verify_reset_email,
    reset_password,
    verify_email,
)


urlpatterns = [
    path("", include("rest_auth.urls")),
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("user-config/", UserConfigView.as_view(), name="user-config"),
    path("verify-id/<str:id>/", verify_id, name="verify_id"),
    path("verify-nickname/<str:nickname>/", verify_nickname, name="verify_nickname"),
    path("verify_email/<str:email>/", verify_email, name="verify_email"),
    path("activate/<str:uidb64>/<str:token>/", activate_user, name="activate"),
    path("send-activation-email/", send_activation_email, name="send_activation_email"),
    path("send-reset-email", password_reset_email, name="send_reset_email"),
    path(
        "verify-reset-email/<str:uidb64>/<str:token>",
        verify_reset_email,
        name="verify_reset_email",
    ),
    path("reset-password", reset_password, name="reset_password"),
]
