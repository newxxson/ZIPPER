"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from zip import views
from usercontrol import views as user_views
router = routers.DefaultRouter()
router.register('areas', views.AreaView, 'area')
router.register('houses', views.HouseView, 'house')
router.register('keywords', views.KeywordView, 'keyword')
router.register('reviews', views.ReviewView, 'review')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("usercontrol/", include('usercontrol.urls')),
    path("api/user-interest/", user_views.UserInterestView.as_view(), name='user-interest'),
    path("api/user-interest/<str:type>/", user_views.UserInterestView.as_view(), name='user-interest-type'),
    path("api/user-interest/<str:type>/<int:pk>/", user_views.UserInterestView.as_view(), name='user-interest-type-pk'),
    
    # path("zip/", include('zip.urls')),
]
