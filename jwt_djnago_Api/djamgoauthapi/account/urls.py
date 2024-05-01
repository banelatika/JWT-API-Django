from django.contrib import admin
from django.urls import path
from account.views import *
urlpatterns = [
    path('reg/', UserRegitsrationvView.as_view(), name = 'register'),
    path('regi/', UserloginView.as_view(), name = 'login'),
    path('profile/', UserprofileView.as_view(), name = 'profile'),
    path('change/', UserChangPpasswordView.as_view(), name = 'change'),
    path('resent/', SendPasswordResetEmailView.as_view(), name = 'resent'),
    path('resend/<uid>/<token>/', SendPasswordResetView.as_view(), name = 'resend'),
    ]

