from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name']

class UserSignupSerializer(serializers.ModelSerializer):
    """User sign up Serializer"""
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "first_name"]
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"].lower(),
            password=validated_data["password"],
            first_name=validated_data["first_name"]
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    """Login Serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError(_("Unable to log in with provided credentials."), code='authorization')
        else:
            raise serializers.ValidationError(_("Must include 'email' and 'password'."), code='authorization')
        data['user'] = user
        return data
    
    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }