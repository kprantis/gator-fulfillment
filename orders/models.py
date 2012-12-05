from django.db import models

class InventoryItem(models.Model):
    """
    Represents a type of inventory item (eg, washers, bolts, etc)/

    name        A descriptive name for the piece of inventory
    image_url   A url to an image of the item
    orderable   True if a item can be directly ordered, False if it is only
                included as a part with another orderable item.
    """
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    orderable = models.BooleanField()

class InventoryItemLink(models.Model):
    """
    Represents a parent-child relationship between two inventory items.

    Some inventory items require additional parts to be sent along.
    Eg, a post may require a certain number of bolts and washers to be
    send along with it for assembly.

    When you order a parent_inventory item, num_child_inventory_items_required
    will also be added to the order.
    """
    parent_inventory_item = models.ForeignKey(InventoryItem, related_name='+')
    child_inventory_item = models.ForeignKey(InventoryItem, related_name='+')
    num_child_inventory_items_required = models.IntegerField()