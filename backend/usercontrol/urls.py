# users/urls.py
from django.urls import include, path
from .views import UserConfigView, CustomLoginView, verify_id, verify_nickname



urlpatterns = [
    path('', include('rest_auth.urls')), 
    path('login/', CustomLoginView.as_view(), name='rest_login'),
    path('user-config/', UserConfigView.as_view(), name='user-config'),
    path('verify-id/<str:id>/', verify_id, name='verify_id'),
    path('verify-nickname/<str:nickname>/', verify_nickname, name='verify_nickname'),
]