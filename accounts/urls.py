from django.urls import path, include
from accounts import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenBlacklistView

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='user_login'),
    path('logout/', TokenBlacklistView.as_view(), name='user_logout'),
    path('signup/', views.RegisterAPIView.as_view(), name='user_signup'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send_verification_code',views.SendCodeViaEmailAPIView.as_view(), name ="send_code"),
    path('verify_code',views.VerifyCodeAPI.as_view(), name = "verify_code")
   

]
