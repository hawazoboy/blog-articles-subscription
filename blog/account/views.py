from django.views import View
from django.views.generic import CreateView, TemplateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .models import User
from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
)
from .services import send_activation_email
from .tokens import account_activation_token


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save(commit=False)

        user.is_verified = False
        user.save()

        token = account_activation_token.make_token(user)

        activation_url = self.request.build_absolute_uri(
            reverse(
                "account:activate",
                kwargs={
                    "uid": user.pk,
                    "token": token,
                },
            )
        )

        send_activation_email(
            user=user,
            activation_url=activation_url,
        )

        return redirect("account:check-email")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )


class ActivateAccountView(View):

    def get(self, request, uid, token):

        user = get_object_or_404(
            User,
            pk=uid
        )

        if account_activation_token.check_token(user, token):
            user.is_verified = True
            user.save(update_fields=["is_verified"])

            return redirect("account:login")

        return redirect("account:register")


class CheckEmailView(TemplateView):
    template_name = "check_email.html"


class LoginView(View):
    template_name = "login.html"

    def get(self, request):

        if request.user.is_authenticated:
            return redirect("/")

        form = LoginForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request):

        if request.user.is_authenticated:
            return redirect("/")

        form = LoginForm(request.POST)

        if form.is_valid():

            user = authenticate(
                request,
                email=form.cleaned_data["email"].lower(),
                password=form.cleaned_data["password"],
            )

            if user is None:

                form.add_error(
                    None,
                    "Invalid email or password.",
                )

            elif not user.is_verified:

                form.add_error(
                    None,
                    "Please verify your email first.",
                )

            else:

                login(
                    request,
                    user,
                )

                next_url = request.GET.get("next")

                if next_url:
                    return redirect(next_url)

                return redirect("/")

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )
    

class LogoutView(View):

    def get(self, request):

        if request.user.is_authenticated:
            logout(request)

        return redirect("/")


class ForgotPasswordView(PasswordResetView):

    form_class = ForgotPasswordForm

    template_name = "reset_password.html"

    email_template_name = "password_reset_email.html"

    subject_template_name = "password_reset_subject.txt"

    success_url = reverse_lazy(
        "account:password_reset_done"
    )


class ForgotPasswordDoneView(
    PasswordResetDoneView
):

    template_name = (
        "password_reset_done.html"
    )


class ResetPasswordConfirmView(
    PasswordResetConfirmView
):

    form_class = (
        ResetPasswordForm
    )

    template_name = (
        "password_reset_confirm.html"
    )

    success_url = reverse_lazy(
        "account:password_reset_complete"
    )


class ResetPasswordCompleteView(
    PasswordResetCompleteView
):

    template_name = (
        "password_reset_complete.html"
    )


class ResendActivationEmailView(View):

    def get(self, request):

        return redirect(
            "account:check-email"
        )

    def post(self, request):

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        user = User.objects.filter(
            email=email,
            is_verified=False,
        ).first()

        if user is None:
            return redirect(
                "account:register"
            )

        token = (
            account_activation_token.make_token(
                user
            )
        )

        activation_url = (
            request.build_absolute_uri(
                reverse(
                    "account:activate",
                    kwargs={
                        "uid": user.pk,
                        "token": token,
                    },
                )
            )
        )

        send_activation_email(
            user=user,
            activation_url=activation_url,
        )

        return redirect(
            "account:check-email"
        )