from rest_framework import serializers
from lms.models import Course, Lesson, Payments, Subscription
from lms.validators import URLValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели подписки """

    class Meta:
        model = Subscription
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        """ Метод проверяет есть ли у текущего пользователя подписка на данный курс """

        request = self.context.get('request')
        user = request.user
        subscription_exists = Subscription.objects.filter(owner=user, course=obj).exists()

        return subscription_exists


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
