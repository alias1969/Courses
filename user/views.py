from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from tutorial.quickstart.serializers import UserSerializer
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Payment, User
from .serializers import PaymentSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from user.services import create_stripe_price, create_stripe_session


class UserViewSet(viewsets.ModelViewSet):
    """API view списка всех пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    """API view создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(ListAPIView):
    """API view списка всех платежей."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_set_fields = (
        "course",
        "lesson",
    )
    ordering_fields = ("date",)
    search_fields = ("method",)


class PaymentCreateAPIView(CreateAPIView):
    """API view нового платежа."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.amount)
        session_id, link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = link
        payment.save()
