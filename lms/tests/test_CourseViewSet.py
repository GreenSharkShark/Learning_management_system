from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course

User = get_user_model()


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.course_data = {'title': 'Test Course', 'description': 'Test Description'}
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        response = self.client.post('/courses/', data=self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_courses(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_course(self):
        course = Course.objects.create(title='Test Course', description='Test Description')
        response = self.client.get(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        updated_data = {'title': 'Updated Title', 'description': 'Updated Description'}
        response = self.client.put(f'/courses/{course.id}/', data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        response = self.client.delete(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
