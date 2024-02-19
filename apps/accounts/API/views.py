from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import renderers, status
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from ...orders.models import Order, OrderItem
from ..models import Address
from .serializers import OrderSerializer, AddressSerializer, OrderItemSerializer

# class OrderListAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderSerializer
#     renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user, status='delivered')
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         data = serializer.data  # Serialized data
#         context = {'order_data': data}
#         return Response(context, template_name='accounts/order_history.html')

class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get_queryset(self):
        delivered_orders = Order.objects.filter(user=self.request.user, status='delivered')
        not_delivered_orders = Order.objects.filter(user=self.request.user).exclude(status='delivered')
        return {
            'delivered_orders': delivered_orders,
            'not_delivered_orders': not_delivered_orders
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        delivered_orders_serializer = self.get_serializer(queryset['delivered_orders'], many=True)
        not_delivered_orders_serializer = self.get_serializer(queryset['not_delivered_orders'], many=True)
        delivered_data = delivered_orders_serializer.data
        not_delivered_data = not_delivered_orders_serializer.data
        context = {
            'delivered_order_data': delivered_data,
            'not_delivered_order_data': not_delivered_data
        }
        return Response(context, template_name='accounts/order_history.html')

class OrderItemListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return OrderItem.objects.filter(order=order)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        context = {'item_data': data}
        return Response(context, template_name='accounts/order_history.html')

# class OrderListAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderSerializer
#     renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
#     def get_queryset(self):
#         response = Order.objects.filter(user=self.request.user, status='delivered')
#         return Response(response, template_name='accounts/order_history.html')
        # return Order.objects.filter(user=self.request.user, status='delivered')


class AddressCreateView(CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(APIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


    def get_serializer_context(self):
        return {'request': self.request}

    def get(self, request, *args, **kwargs):
        address = self.get_object()
        serialized_data = self.serializer_class(address, context=self.get_serializer_context()).data
        return Response(serialized_data)


    def get_object(self):
        try:
            return Address.objects.get(pk=self.kwargs['pk'], user=self.request.user)
        except Address.DoesNotExist:
            raise NotFound()

    def put(self, request, pk):
        address = self.get_object()
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object()
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressListView(ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        addresses = self.get_queryset()
        serialized_data = self.serializer_class(addresses, many=True).data
        return JsonResponse({'addresses': serialized_data})

class PanelView(TemplateView):
    template_name = 'accounts/panel.html'