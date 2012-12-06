from django.http import HttpResponse

def label(request, order_id):
    return HttpResponse("Create a label for order_id %s" % order_id)
