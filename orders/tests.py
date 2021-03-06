"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from inventory.models import InventoryItem, InventoryItemLink
from orders.models import Order


class OrdersTest(TestCase):
    fixtures = ['test_inventory.json']

    def test_generating_a_set_of_labels(self):
        # Create an order for 5 posts
        order = Order.objects.create(
            description = "A test order"
        )

        post = InventoryItem.objects.get(name='Post')

        order.orderitem_set.create(
            order = order,
            inventory_item = post,
            quantity = 5
        )

        self.assertEqual(5, order.orderitem_set.get(pk=1).quantity)

        # Verify the quantities all come out as expected
        labels = order.generate_labels()
        
        post_labels = [l for l in labels if l.name == "Post"]
        self.assertEqual(3, len(post_labels), post_labels)
        self.assertEqual(2, 
            len([l for l in post_labels if l.quantity == "Box of 2"]))
        self.assertEqual(1,
            len([l for l in post_labels if l.quantity == "Box of 1"]))

        anchor_labels = [l for l in labels if l.name == "Concrete Anchor"]
        self.assertEqual(2, len(anchor_labels), anchor_labels)
        self.assertEqual(1,
            len([l for l in anchor_labels if l.quantity == "Bag of 100"]))
        self.assertEqual(1,
            len([l for l in anchor_labels if l.quantity == "Bag of 25"]))

        washer_labels = [l for l in labels if l.name == "Flat Washers"]
        self.assertEqual(1, len(washer_labels), washer_labels)
        self.assertEqual("Bag of 50", washer_labels[0].quantity)

        screw_labels = [l for l in labels if l.name == "Safety Screw"]
        self.assertFalse(screw_labels,
            "Parent comes preassembled - should not have a label generated, but found [%s]" % [l.name for l in screw_labels])

    def test_generating_a_hardware_order_form(self):
        # Create an order for 5 posts
        order = Order.objects.create(
            description = "A test order"
        )

        post = InventoryItem.objects.get(name='Post')

        order.orderitem_set.create(
            order = order,
            inventory_item = post,
            quantity = 5
        )

        self.assertEqual(5, order.orderitem_set.get(pk=1).quantity)

        # Verify the quantities all come out as expected
        items = order.generate_hardware_order_form_items()
        
        post_items = [i for i in items if i.name == "Post"]
        self.assertEqual(1, len(post_items), post_items)
        self.assertEqual(5, post_items[0].quantity)

        anchor_items = [i for i in items if i.name == "Concrete Anchor"]
        self.assertEqual(1, len(anchor_items), anchor_items)
        self.assertEqual(125, anchor_items[0].quantity)

        washer_items = [i for i in items if i.name == "Flat Washers"]
        self.assertEqual(1, len(washer_items), washer_items)
        self.assertEqual(50, washer_items[0].quantity)

        screw_items = [i for i in items if i.name == "Safety Screw"]
        self.assertEqual(1, len(screw_items), screw_items)
        self.assertEqual(250, screw_items[0].quantity)
