import json
from .models import *

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items # Remove the parentheses here

    else:
        items = []
        cartItems = 0  # Assign a default value for unauthenticated users
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    return {'cartItems': cartItems, 'order': order, 'items': items}