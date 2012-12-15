from django.shortcuts import render
from django.template import Context, loader

from orders.models import Order

def label(request, order_id):
    """
    Create a printable sheet of labels for each of the items associated
    with a order.
    """
    order = Order.objects.get(pk=order_id)
    labels = order.generate_labels()

    context = {'labels' : labels}
    return render(request, 'orders/label.html', context)
