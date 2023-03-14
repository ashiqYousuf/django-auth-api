from django.urls import path
from .views import UserRegistrationView , UserLoginView , UserProfileView , UserChangePasswordView , SendPasswordResetEmailView , UserPasswordResetView , UserChangeProfileView

urlpatterns = [
    path('register/' , UserRegistrationView.as_view(),name="register"),
    path('login/' , UserLoginView.as_view(),name="login"),
    path('profile/' , UserProfileView.as_view(),name="profile"),
    path('changepassword/' , UserChangePasswordView.as_view(),name="changepassword"),
    path('send-reset-password-email/' , SendPasswordResetEmailView.as_view(),name="send-reset-password-email"),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view() , name="reset-password"),
    path('changeprofile/',UserChangeProfileView.as_view() , name='changeprofile'),
]
