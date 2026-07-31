from django.test import TestCase
from django.urls import reverse

from contact.models import ContactUs


class ContactViewTests(TestCase):
    def test_contact_page_status_code_200(self):
        response = self.client.get(reverse("contact:contact_us"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_uses_correct_template(self):
        response = self.client.get(reverse("contact:contact_us"))
        self.assertTemplateUsed(response, "contact.html")

    def test_valid_contact_form_creates_contact_message(self):
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Subject",
            "message": "Test message body",
        }

        response = self.client.post(reverse("contact:contact_us"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactUs.objects.count(), 1)
        self.assertEqual(ContactUs.objects.first().name, "Test User")
        self.assertEqual(ContactUs.objects.first().email, "test@example.com")
   # Tests updated by Test Manager (Rami)
   # Verified contact app responses
