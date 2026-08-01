from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from article.models import Category, Post

class HomeViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@gmail.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.category = Category.objects.create(title="Technology")
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            body="This is a test post body.",
            image="images/articles/test.jpg",
        )
        self.post.category.add(self.category)

    def test_home_view_status_code_200(self):
        response = self.client.get(reverse("home:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse("home:home"))
        self.assertTemplateUsed(response, "home/index.html")

    def test_home_view_passes_posts_to_context(self):
        response = self.client.get(reverse("home:home"))
        self.assertIn("posts", response.context)
        self.assertIn(self.post, response.context["posts"])
   # Tests updated by Test Manager (Rami)
   # Verified contact app responses
