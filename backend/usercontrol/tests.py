from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status  # Replace with your actual User model import
from .utils import (
    is_time_interval_ok,
    send_activation_email,
)  # Replace with your actual import
from django.contrib.auth import get_user_model


class EmailVerificationTest(TestCase):
    def setUp(self)
        self.new_email = "newxxson@korea.ac.kr"
        self.existing_email = "test@korea.ac.kr"

    def test_verify_email_with_new_email_and_time_ok(self):
        url = reverse("verify_email", kwargs={"email": self.new_email})

        with self.subTest("Test time interval"):
            self.assertTrue(is_time_interval_ok(self.new_email))

        with self.subTest("Test send activation email"):
            send_activation_email(
                self.new_email
            )  # You may check sent emails if implemented to do so

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "activation email sent"})

    def test_verify_email_with_new_email_and_time_not_ok(self):
        url = reverse("your_url_name", kwargs={"email": self.new_email})

        with self.subTest("Test time interval"):
            self.assertFalse(
                is_time_interval_ok(self.new_email)
            )  # Assuming the interval is too short

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"message": "you need to wait to send another mail"}
        )
