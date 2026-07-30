from django.urls import path
from .views import *

app_name = "account"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("ativate/<int:uid>/<str:token>/", ActivateAccountView.as_view(), name="activate"),
    path("check_email/", CheckEmailView.as_view(), name="check-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", ForgotPasswordView.as_view(), name="password_reset"),
    path("password-reset/done/", ForgotPasswordDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", ResetPasswordConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", ResetPasswordCompleteView.as_view(), name="password_reset_complete"),
    path("resend-email/", ResendActivationEmailView.as_view(), name="resend-email"),
]