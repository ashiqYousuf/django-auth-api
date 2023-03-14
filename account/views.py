from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer , UserLoginSerializer , UserProfileSerializer , UserChangePasswordSerializer , SendPasswordResetEmailSerializer , UserPasswordResetSerializer , UserChangeProfileSerializer
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User

# Generating Tokens Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request , format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {
                'msg': 'registration successfull',
                'token': token
            },
            status=status.HTTP_201_CREATED
        )

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request , format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email , password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response(
                {
                    'msg': 'Login Success',
                    'token': token,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'errors': {'non_field_errors':['Email or Password is not valid']}},
                status=status.HTTP_404_NOT_FOUND
            )


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self , request , format=None):
        # Converting Complex Type into python native => Serialization
        # request.user => User.objects.get(pk=request.user.id)
        # But request.user must not be Anonymous User
        serializer = UserProfileSerializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self , request , format=None):
        # Sending context to the UserChangePasswordSerializer
        serializer = UserChangePasswordSerializer(data=request.data , context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response(
            {'msg': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request , format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link sent. Please check your Email"},
            status=status.HTTP_200_OK
        )

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request , uid , token , format=None):
        # We need to access ID & Token to know which user is requesting for password reset
        context = {
            'uid': uid,
            'token': token,
        }
        serializer = UserPasswordResetSerializer(data=request.data , context=context)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'msg': 'Password Reset Successfully'},
            status=status.HTTP_200_OK
        )


# Adding Extra Functionality

class UserChangeProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        serializer = UserChangeProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.user.email)
        user.name = serializer.data.get('name')
        user.tc = serializer.data.get('tc')
        user.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
