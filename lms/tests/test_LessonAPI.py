from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson

User = get_user_model()


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.lesson_data = {
            "title": "Test Lesson",
            "description": "Test Description",
            "video_url": "https://www.youtube.com/",
        }
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        response = self.client.post('/lesson/create/', data=self.lesson_data, owner=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        response = self.client.get('/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson(self):
        lesson = Lesson.objects.create(**self.lesson_data)
        response = self.client.get(f'/lesson/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)
        updated_data = {
            "title": "Updated tile",
            "description": "Updated Description",
            "video_url": "https://www.youtube.com/",
        }
        response = self.client.put(f'/lesson/update/{lesson.id}/', data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)
        response = self.client.delete(f'/lesson/delete/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
