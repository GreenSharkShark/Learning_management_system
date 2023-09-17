import stripe
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from config import settings
from lms.models import Course, Lesson, Payments, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from lms.permissions import IsOwnerOrReadOnly, IsOwner, StaffDenied
from lms.services import generate_payment_intent, get_payment_status
from users.models import User
from lms.paginators import LMSPaginator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LMSPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, StaffDenied]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LMSPaginator


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
    permission_classes = [IsAuthenticated, IsOwner, StaffDenied]


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'cash_payment')
    ordering_fields = ('payment_date',)

    def perform_create(self, serializer):
        amount = self.request.data.get('payment_amount')
        payment_intent = generate_payment_intent(amount)
        user = self.request.user
        paid_lesson = self.request.data.get('paid_lesson')
        paid_course = self.request.data.get('paid_course')
        serializer.save(paid_lesson=paid_lesson, paid_course=paid_course, user=user)

        payment_status = get_payment_status(payment_intent['id'])

        if payment_status.status == 'requires_payment_method':
            return Response({'message': 'Пожалуйста, завершите оплату.'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        elif payment_status.status == 'succeeded':
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Произошла ошибка при обработке платежа.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
