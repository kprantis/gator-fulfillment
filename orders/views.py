import logging
import os
import sys
import textwrap
import traceback
import urllib2

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from StringIO import StringIO 

from orders.models import Order


logger = logging.getLogger('orders')
logger.setLevel(logging.ERROR)
stdout_handler = logging.StreamHandler(sys.stderr)
file_handler = logging.FileHandler("orders.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


class LabelTypes(object):
    LABEL_TYPE_SHIPPING = 'shipping'
    LABEL_TYPE_PACKING = 'packing'


def generate_labels_pdf(order_id, labels, label_type):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="labels_%s_order_%s.pdf"' % (label_type, order_id)

    canv = canvas.Canvas(response, pagesize=LETTER )
    canv.setPageCompression( 0 )

    # Spacing in points, bottom left = 0, 0
    # top right = 612, 792

    LABELW = 2.625 * inch
    LABELSEP = 2.75 * inch
    LABELH = 1 * inch
    BASE_Y_DIFF = 19

    def LabelPosition(ordinal):
        y,x = divmod(ordinal, 3)
        x = 14 + x * LABELSEP
        y = 756 - y * LABELH
        return x, y

    def printLines(tx, font_size, lines):
        num_chars_in_line = 250/font_size
        print_lines = []
        for line in lines:
            print_lines.extend(textwrap.wrap(line, num_chars_in_line) or [''])
        assert print_lines
        tx.textLines(print_lines)
        canv.drawText(tx)
        return (len(print_lines) - 1) * font_size

    row_num = 0
    label_num = 1
    for label in labels:
        x, y = LabelPosition( row_num )
        #canv.rect( x, y, LABELW, -LABELH )
        current_y_diff = BASE_Y_DIFF
        tx = canv.beginText( x+2, y-current_y_diff )
        if label_type == LabelTypes.LABEL_TYPE_SHIPPING:
            tx.setFillColor("green")
        elif label_type == LabelTypes.LABEL_TYPE_PACKING:
            tx.setFillColor("blue")
        else:
            raise RuntimeError("Unrecognized label type: '%s'" % label_type)
        tx.setFont( 'Times-Bold', 14, 14 )
        current_y_diff += printLines(tx, 14, [label.name]) + 11
        tx = canv.beginText( x+2, y-current_y_diff )
        tx.setFillColor('black')
        tx.setFont( 'Times-Roman', 11, 11 )
        current_y_diff += printLines(tx, 11, [label.description, label.relationship]) + 14
        tx = canv.beginText( x+2, y-current_y_diff )
        tx.setFont( 'Times-Bold', 14, 14 )
        printLines(tx, 14, [label.quantity])

        current_y_diff = BASE_Y_DIFF  # moving to a new column
        if label.image_url:
            image_name = label.image_url.rsplit('/', 1)[-1]
            try:
                if not os.path.exists(image_name):
                    f = open(image_name, 'w')
                    f.write(urllib2.urlopen(label.image_url).read())
                    f.close()
                canv.drawImage(image_name, x+LABELW-71, y-71, 70, 70)
            except Exception, e:
                # Don't want to disrupt the whole page if one image has a problem, so
                # we just log the error and display that there was an error for that img.
                exception_type, value, trace = sys.exc_info()
                logger.error('\n'.join(traceback.format_exception(exception_type, value, trace)))
                tx = canv.beginText(x+LABELW-71, y-current_y_diff)
                printLines(tx, 14, ["ERROR", "Loading", "Image"])
                try:
                    # Remove img in case it is corrupt so it will be
                    # re-fetched next time.
                    os.remove(image_name)
                except Exception, e:
                    exception_type, value, trace = sys.exc_info()
                    logger.error('\n'.join(traceback.format_exception(exception_type, value, trace)))
        if label_num > 1 and label_num % 30 == 0:
            canv.showPage()
            row_num = -1
        label_num += 1
        row_num +=1

    # Close the PDF object cleanly, and we're done.
    canv.save()
    return response

def label(request, order_id):
    """
    Create a printable sheet of labels for each of the items associated
    with a order to go on the individual packages of items.
    """
    order = Order.objects.get(pk=order_id)
    labels = order.generate_labels()

    return generate_labels_pdf(order_id, labels, LabelTypes.LABEL_TYPE_SHIPPING) 

def packing_label(request, order_id):
    """
    Create a printable sheet of labels for each of the items associated
    with a order to go onto the outer packing.
    """
    order = Order.objects.get(pk=order_id)
    labels = order.generate_labels()

    return generate_labels_pdf(order_id, labels, LabelTypes.LABEL_TYPE_PACKING)

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
