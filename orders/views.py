from django.shortcuts import render
from django.template import Context, loader

from orders.models import Order

def label(request, order_id):
    """
    Create a printable sheet of labels for each of the items associated
    with a order to go on the individual packages of items.
    """
    order = Order.objects.get(pk=order_id)
    labels = order.generate_labels()

    context = {'labels' : labels}
    return render(request, 'orders/label.html', context)

def packing_label(request, order_id):
    """
    Create a printable sheet of labels for each of the items associated
    with a order to go onto the outer packing.
    """
    order = Order.objects.get(pk=order_id)
    labels = order.generate_labels()

    context = {'labels' : labels}
    return render(request, 'orders/packing_label.html', context)

def hardware_order_form(request, order_id):
    """
    Create a printable master list of all the components going
    into an order, even if going to be pre-assembled.
    """
    order = Order.objects.get(pk=order_id)
    hardware_order_form_items = order.generate_hardware_order_form_items()

    context = {
        'order': order,
        'hardware_order_form_items' : hardware_order_form_items
    }
    return render(request, 'orders/hardware_order_form.html', context)
