from rest_framework import serializers
from accounts.models  import User, EmailVerificationCode
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if (not username.isalnum()):

            raise serializers.ValidationError(
                self.default_error_messages)
        
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
    



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8,write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    
    class Meta:
        model = User
        fields = ['password','username','tokens']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise AuthenticationFailed('Username and password are required')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.in_blocklist():
                raise AuthenticationFailed('User is currently blocked')
            else:
                user.handle_success_login()
                return {
                    'email': user.email,
                    'username': user.username,
                    'tokens': user.tokens
                }
        else:
            try:
                user = User.objects.get(username=username)
                if user.in_blocklist():
                    raise AuthenticationFailed('User is currently blocked')
                else:
                    user.user_attempts -= 1
                    if user.user_attempts == 0:
                        user.block()
                        raise AuthenticationFailed('Invalid credentials. User has been blocked for 1 hour')
                    else:
                        user.save()
                        raise AuthenticationFailed('Invalid credentials, try again')
            except User.DoesNotExist:
                raise AuthenticationFailed('Invalid credentials, try again')



class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationCode
        fields = ('email',)