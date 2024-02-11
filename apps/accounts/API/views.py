from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from ...orders.models import Order
from ..models import Address
from .serializers import OrderSerializer, AddressSerializer

class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='delivered')

class AddressCRUDViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
