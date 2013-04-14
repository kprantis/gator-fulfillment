"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from inventory.models import InventoryItem, InventoryItemLink


class InventoryModelTest(TestCase):

    def test_can_create_inventory_items(self):
        # Make sure we are starting with the expected empty tables.
        self.assertFalse(InventoryItem.objects.all())
        self.assertFalse(InventoryItemLink.objects.all())
        
        # Add two inventory items
        parent_item = InventoryItem.objects.create(
            name = "Parent", 
            image_url = '',
            max_per_container = 5,
            orderable = True
        )
        child_item = InventoryItem.objects.create(
            name="Child",
            image_url='',
            max_per_container = 5,
            orderable = False
        )
        self.assertEqual(2, len(InventoryItem.objects.all()))
        self.assertTrue(parent_item.orderable)
        
        # Link the items into a parent-child relationship where the
        # parent item requires a certain number of child items.
        item_link = InventoryItemLink.objects.create(
            parent_inventory_item = parent_item,
            child_inventory_item = child_item,
            num_child_inventory_items_required = 5
        )
        self.assertEqual(1, len(InventoryItemLink.objects.all()))
        self.assertEqual('Parent', item_link.parent_inventory_item.name)
        self.assertEqual('Child', item_link.child_inventory_item.name)
