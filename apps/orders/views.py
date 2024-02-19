import json
from .models import Order, OrderItem
from django.utils.crypto import get_random_string
from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import TemplateView, View, DetailView, FormView
from ..accounts.models import User, Address
from ..products.models import Product, Discount
from .forms import AddressSelectionForm

# Create your views here.

class SelectAddressView(FormView):
    template_name = 'orders/select_address.html'
    form_class = AddressSelectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        selected_address_id = form.cleaned_data['address']
        selected_address = Address.objects.get(id=selected_address_id)
        return HttpResponseRedirect(reverse('orders:cart:order_registration', args=[selected_address_id]))


# class SaveOrderView(View):
#     def post(self, request, *args, **kwargs):
#         product_details = request.COOKIES.get('shopping_cart')
#         if not product_details:
#             return JsonResponse({'error': 'No product details found in cookies'}, status=400)
#
#         product_details = eval(product_details)  # این برای استرینگ به دیکشنریه
#
#         selected_address_id = request.POST.get('address')
#         if not selected_address_id:
#             return JsonResponse({'error': 'No address selected'}, status=400)
#
#         try:
#             selected_address = Address.objects.get(id=selected_address_id)
#         except Address.DoesNotExist:
#             return JsonResponse({'error': 'Selected address does not exist'}, status=400)
#
#         order = Order.objects.create(user=request.user, address=selected_address.complete_address, total_price=0,
#                                      discounted_total_price=0, is_paid=True)
#
#         total_price = 0
#         discounted_total_price = 0
#
#         for item in product_details:
#             product_id = item['product_id']
#             quantity = item['quantity']
#             name = item['name']
#             price = item['price']
#
#             item_total_price = price * quantity
#             total_price += item_total_price
#
#             discount = item.get('discount', None)
#             if discount:
#                 discounted_price = item_total_price - discount.amount
#                 discounted_total_price += discounted_price
#             else:
#                 discounted_total_price += item_total_price
#
#             OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity)
#
#         order.total_price = total_price
#         order.discounted_total_price = discounted_total_price
#         order.save()
#
#         return render(request, 'orders/order_registration_result.html')


