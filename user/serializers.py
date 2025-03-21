from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer для платежей"""
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Serializer для пользователя"""
    # Отображаем платежи пользователя
    payments = PaymentSerializer(source="payments_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
