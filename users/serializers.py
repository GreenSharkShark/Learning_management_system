from rest_framework import serializers
from lms.serializers import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'id', 'payments', 'email', 'avatar', 'phone', 'country', 'first_name', 'last_name']
