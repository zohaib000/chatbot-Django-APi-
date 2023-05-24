from django.contrib import admin
from django.urls import path, include
from home import views
from .views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name="register"),
    path('login', UserLoginView.as_view(), name="login"),
    path('profile', UserProfileView.as_view(), name="profile"),
    path('profileData', profileData.as_view(), name="profileData"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # payment related
    path('create-checkout-session', Payment.as_view(), name="Payment"),
    path('create-portal-session', customer_portal.as_view(), name="customer_portal"),
    path('webhook_received', webhook_received.as_view(),
         name="webhook_received"),

    # to chatgpt response
    path('Conversation', Conversation.as_view(), name="Conversation"),
    path('getChatHistory', getChatHistory.as_view(), name="getChatHistory"),

    # custom models
    path('createPrompt', createPrompt.as_view(), name="createPrompt"),
    path('savePrompt', savePrompt.as_view(), name="savePrompt"),
    path('getPrompt/<int:pk>', getPrompt.as_view(), name="getPrompt"),
    path('getPrompts', getPrompts.as_view(), name="getPrompts"),
    path('getUserPrompts/<str:email>',
         getUserPrompts.as_view(), name="getUserPrompts"),
    path('searchPrompt', searchPrompt.as_view(), name="searchPrompt"),
    path('searchSavedPrompt', searchSavedPrompt.as_view(),
         name="searchSavedPrompt"),
    path('getSavedPrompts', getSavedPrompts.as_view(), name="getSavedPrompts"),
    path('increaseView', increaseView.as_view(), name="increaseView"),

    # profile picture
    path('uploadProfilePicture', uploadProfilePicture.as_view(),
         name="uploadProfilePicture"),



]
