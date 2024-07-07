import jwt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
    EmailVerificationSerializer,
)
from accounts.models import User, EmailVerificationCode

# Create your views here.


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data
        print(user['username'])
        # getting tokens
        user_data = User.objects.get(email=user["email"])
        tokens = RefreshToken.for_user(user_data).access_token

        # send email for user verification
       

        return Response(
            {"The registration is completed successfuly."},
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendCodeViaEmailAPIView(APIView):
    serializer_class = EmailVerificationSerializer
    def post(self,request):
        serializer= self.serializer_class(data = request.data)
        if serializer.is_valid():
            EmailVerificationCode.objects.update_or_create(
                email= serializer.data['email'],
                defaults={
                    'email':serializer.data['email']
                }
                )
            
            user_data = EmailVerificationCode.objects.get(email = serializer.data['email'])
    

            return Response(
                    {"success": "Success! Check your email for the code.", "verify_code":user_data.code}
                )
        
        return Response({"error":"Validation failed"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeAPI(APIView):
    def post(self, request):
        email = request.data['email']
        code = request.data['code']
        if EmailVerificationCode.objects.filter(email=email,code=code).exists():
            user = User.objects.get(email = email)
            user.is_verified = True
            return Response({"success":"Code Successfully Verified."})
        else:
            return Response({"error":"Code doesnot match."}, status=status.HTTP_404_NOT_FOUND)