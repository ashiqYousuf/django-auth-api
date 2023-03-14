from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str , force_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

# Serializer to reset password need password and confirm_password  Field [No Need to be a Model Serializer]
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    class Meta:
        fields = ['password' , 'password2']

    def validate(self , attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            # Need uid and token from the context to know which user is requesting for password change
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confirm password does'nt match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            # Check the Equality of the incoming token and the token generated for user
            if not PasswordResetTokenGenerator().check_token(user , token):
                raise serializers.ValidationError("Invalid or Expired Token")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user , token)
            raise serializers.ValidationError("Invalid or Expired Token")


# Serializer for reseting password need Email Field [No Need to be a Model Serializer]
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    def validate(self , attrs):
        email = attrs.get('email')
        # Checking if the Email Exists in the Database
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # encoding user id sending it in url
            uid = urlsafe_base64_encode(force_bytes(user.id)) # takes byte object not integer as param
            # Password Reset Token
            token = PasswordResetTokenGenerator().make_token(user)
            # Generate Password Reset Link from uid and token
            link = f'http://localhost:3000/api/user/reset-password/{uid}/{token}'
            # Sending Email to the User
            body = f'Click the link to reset your password {link}'
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('User not resgistered')



# Serializer For Password Change [No need to be a Model Serializer]
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    class Meta:
        fields = ['password' , 'password2']

    def validate(self , attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password does'nt match")
        # I need user to set it's password user.set_password() and save it as user.save()
        # So we need to send request.user to the serializer
        user.set_password(password)
        user.save()
        return attrs


# Serializer for Profile [ModelSerializer]
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'email' , 'name']


# Serializer For Registration [Must be a Model Serializer]
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email' , 'name' , 'tc' , 'password' , 'password2']
        extra_kwargs = {
            'password':{
                'write_only': True
            }
        }

    def validate(self , attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError("password and confirm password does'nt match")
        return attrs

    # Since we are dealing with custom Model User , define create method
    def create(self , validate_data):
        return User.objects.create_user(**validate_data)

# Serializer for Login [can be a simple Serializer or a ModelSerializer]
# Better to validate | authenticate user in the views than here overriding validate() method
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email' , 'password']


class UserChangeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name' , 'tc']

