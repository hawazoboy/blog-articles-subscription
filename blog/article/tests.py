from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Post, Category, PostLike


class ArticleTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )

        self.category = Category.objects.create(title="Python")

        # یک فایل تصویر خیلی کوچک (fake)
        image_file = SimpleUploadedFile(
            name="test.jpg",
            content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b",
            content_type="image/jpeg",
        )

        # اگر در مدل Post فیلد image اجباری نیست، همین کافی است.
        # اگر اجباری است، حتماً باید ست شود.
        self.post = Post.objects.create(
            title="Django Testing",
            slug="django-testing",
            author=self.user,
            body="This is a test post.",
            image=image_file,   # اگر نام فیلد متفاوت است اصلاحش کن
        )
        self.post.category.add(self.category)

    def test_all_articles_view(self):
        response = self.client.get(reverse("article:all_articles"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "all_articles.html")
        self.assertIn("all_articles", response.context)

    def test_article_detail_view(self):
        response = self.client.get(reverse("article:detail", kwargs={"slug": self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "article_detail.html")
        self.assertEqual(response.context["article"].slug, "django-testing")

    def test_search_articles(self):
        response = self.client.get(reverse("article:search_articles"), {"q": "Django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Testing")

    def test_like_post_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("article:like_post", kwargs={"slug": self.post.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["liked"], True)
        self.assertEqual(PostLike.objects.count(), 1)

    def test_like_post_unauthenticated_redirects(self):
        response = self.client.get(reverse("article:like_post", kwargs={"slug": self.post.slug}))
        self.assertEqual(response.status_code, 302)
   # Tests updated by Test Manager (Rami)
   # Verified contact app responses
