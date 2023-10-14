from rest_framework import serializers
from lms.serializers import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'id', 'payments', 'email', 'avatar', 'phone', 'country', 'first_name', 'last_name']

    def to_representation(self, instance):
        request = self.context.get('request')
        user = request.user

        if user == instance:  # Если текущий пользователь является владельцем профиля
            return super().to_representation(instance)
        else:
            # Возвращаем все поля кроме 'username', 'payments' и 'last_name'
            return {
                'id': instance.id,
                'email': instance.email,
                'avatar': instance.avatar if instance.avatar else None,
                'phone': instance.phone,
                'country': instance.country,
                'first_name': instance.first_name,
            }
