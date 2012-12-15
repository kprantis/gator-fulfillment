from django.http import HttpResponse
from django.template import Context, loader

from orders.models import Order

def label(request, order_id):
    """
    Create a printable sheet of labels for each of the items associated
    with a order.
    """
    order = Order.objects.get(pk=order_id)

    template = loader.get_template('orders/label.html')
    context = Context({
        'order' : order
    })
    return HttpResponse(template.render(context))
