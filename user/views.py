from datetime import datetime

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from user.services import create_stripe_price, create_stripe_session


class UserViewSet(viewsets.ModelViewSet):
    """API view списка всех пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=('post,'))
    def last_login(self, pk):
        user = get_object_or_404(User, pk=pk)
        if user:
            user.last_login = datetime.now()
            user.save()

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
