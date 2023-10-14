from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Subscription

User = get_user_model()


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.subscription_data = {
            "owner": self.user.id,
            "course": self.course.id,
        }
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        response = self.client.post('/course/subscribe/', data=self.subscription_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_subscription(self):
        subscription = Subscription.objects.create(owner=self.user, course=self.course)
        response = self.client.delete(f'/course/subscription-delete/{subscription.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
