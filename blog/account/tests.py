from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from .tokens import account_activation_token

User = get_user_model()

class AccountTests(TestCase):
    def setUp(self):
        # ساخت یک کاربر نمونه برای تست‌های لاگین و فعال‌سازی
        self.user_password = "TestPassword123!"
        self.user = User.objects.create_user(
            email="existing@test.com",
            password=self.user_password,
            first_name="Rami",
            last_name="Student",
            is_verified=False  # طبق منطق شما ابتدا تایید نشده است
        )

    def test_register_view_get(self):
        """بررسی باز شدن صفحه ثبت‌نام"""
        response = self.client.get(reverse("account:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_post_success(self):
        """تست ثبت‌نام موفق و ارسال ایمیل فعال‌سازی"""
        data = {
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@test.com",
            "password1": "NewPass123!",
            "password2": "NewPass123!",
        }
        response = self.client.post(reverse("account:register"), data)
        
        # بعد از ثبت‌نام موفق به check-email ریدایرکت می‌شود
        self.assertRedirects(response, reverse("account:check-email"))
        # بررسی ایجاد کاربر در دیتابیس
        self.assertTrue(User.objects.filter(email="newuser@test.com").exists())
        # بررسی ارسال ایمیل (outbox باید یک عضو داشته باشد)
        self.assertEqual(len(mail.outbox), 1)

    def test_activate_account_success(self):
        """تست تایید حساب کاربری با توکن صحیح"""
        token = account_activation_token.make_token(self.user)
        url = reverse("account:activate", kwargs={"uid": self.user.pk, "token": token})
        
        response = self.client.get(url)
        
        # رفرش کردن کاربر از دیتابیس برای چک کردن تغییر فیلد
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.assertRedirects(response, reverse("account:login"))

    def test_activate_account_invalid_token(self):
        """تست عدم تایید با توکن اشتباه"""
        url = reverse("account:activate", kwargs={"uid": self.user.pk, "token": "wrong-token"})
        response = self.client.get(url)
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verified)
        self.assertRedirects(response, reverse("account:register"))

    def test_login_success(self):
        """تست لاگین موفق کاربر تایید شده"""
        self.user.is_verified = True
        self.user.save()
        
        data = {"email": self.user.email, "password": self.user_password}
        response = self.client.post(reverse("account:login"), data)
        
        self.assertRedirects(response, "/")
        # بررسی اینکه کاربر واقعاً در سیستم لاگین شده است
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_fail_not_verified(self):
        """کاربر تایید نشده نباید بتواند لاگین کند"""
        data = {"email": self.user.email, "password": self.user_password}
        response = self.client.post(reverse("account:login"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please verify your email first.")

    def test_logout(self):
        """تست خروج از حساب کاربری"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account:logout"))
        self.assertRedirects(response, "/")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_resend_activation_email(self):
        """تست ارسال مجدد ایمیل فعال‌سازی"""
        data = {"email": self.user.email}
        response = self.client.post(reverse("account:resend-email"), data)
        
        self.assertRedirects(response, reverse("account:check-email"))
        self.assertEqual(len(mail.outbox), 1)
        
   # Tests updated by Test Manager (Rami)
   # Verified contact app responses
