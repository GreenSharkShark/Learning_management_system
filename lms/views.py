from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from lms.models import Course, Lesson, Payments, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from lms.permissions import IsOwnerOrReadOnly, IsOwner
from users.models import User


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'cash_payment')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Класс для создания подписки """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.request.data.get('owner'))
        course = get_object_or_404(Course, pk=self.request.data.get('course'))

        serializer.save(owner=user, course=course)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """ Класс для удаления подписки """
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
