from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import renderers, status, viewsets
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from ...orders.models import Order, OrderItem
from ..models import Address, User, Profile
from .serializers import OrderSerializer, AddressSerializer, OrderItemSerializer, UserSerializer, ProfileSerializer

# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         queryset = User.objects.all()
#         return queryset
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = UserSerializer(queryset, many=True)
#         data = serializer.data
#         return Response({'user_data': data}, status=status.HTTP_200_OK)

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


class AddressListView(APIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        addresses = self.get_queryset()
        serialized_data = self.serializer_class(addresses, many=True).data
        return Response({'addresses': serialized_data})

class AddressCreateView(APIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, address_id, format=None):
        address = get_object_or_404(Address, id=address_id)
        address.delete()
        return Response({'message': 'Address deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class AddressEditView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, address_id, format=None):

        address = get_object_or_404(Address, id=address_id)


        serializer = AddressSerializer(address, data=request.data)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class ProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id, format=None):
        # Filter users by their ID
        user_info = get_object_or_404(User, id=user_id)
        profile_info = get_object_or_404(Profile, user=user_info)

        user_serializer = UserSerializer(user_info, data=request.data)
        profile_serializer = ProfileSerializer(profile_info, data=request.data)

        # if user_serializer.is_valid() and profile_serializer.is_valid() :
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PanelView(TemplateView):
    template_name = 'accounts/panel.html'