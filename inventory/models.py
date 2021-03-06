from django.db import models

class InventoryItem(models.Model):
    """
    Represents a type of inventory item (eg, washers, bolts, etc)/

    name                A descriptive name for the piece of inventory
    description         An optional additional description of the item
    image_url           A url to an image of the item
    orderable           True if a item can be directly ordered, False if
                        only included as a part w/another orderable item.
    container_type      The type of container the inventory item will be
                        shipped in
    max_per_container   The maximum number of these items that can fit
                        into one container as specified by container_type
    required_items      A many-to-many relationship - see InventoryItemLink
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    item_number = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True)
    container_type = models.CharField(max_length=200)
    max_per_container = models.IntegerField()
    orderable = models.BooleanField()
    preassembled = models.BooleanField()
    required_items = models.ManyToManyField(
        "self",
        through = 'InventoryItemLink',
        symmetrical = False
    )

    def __unicode__(self):
        return u"%s%s" % (
            self.name, 
            " (%s)" % self.description if self.description else ''
        )

class InventoryItemLink(models.Model):
    """
    Represents a parent-child relationship between two inventory items.

    Some inventory items require additional parts to be sent along.
    Eg, a post may require a certain number of bolts and washers to be
    send along with it for assembly.

    When you order a parent_inventory item, num_child_inventory_items_required
    will also be added to the order. Description describes what the child
    part is used for (ex, a concrete anchor may be a part os a foot assembly)
    """
    parent_inventory_item = models.ForeignKey(InventoryItem, related_name='+')
    child_inventory_item = models.ForeignKey(InventoryItem, related_name='+')
    num_child_inventory_items_required = models.IntegerField()
    relationship = models.CharField(max_length=200, blank=True, verbose_name="Part relationship")

    def __unicode__(self):
        return u"A %s requires %s %s%s for the %s" % (
            self.parent_inventory_item,
            self.num_child_inventory_items_required,
            self.child_inventory_item,
            's' if self.num_child_inventory_items_required > 1 else '',
            self.relationship
        )

class Label(object):
    """
    Container for the data necessary for a print label to be packaged
    along with an inventory item.
    """
    def __init__(self, inventory_item, relationship, quantity):
        self.name = inventory_item.name
        self.description = inventory_item.description
        self.image_url = inventory_item.image_url
        self.relationship = relationship
        self.quantity = "%s of %s" % (
            inventory_item.container_type,
            quantity
        )

class HardwareOrderFormItem(object):
    """
    Container for the data for an item on the hardware order form.
    """
    def __init__(self, inventory_item, quantity):
        self.name = inventory_item.name
        self.description = inventory_item.description
        self.item_number = inventory_item.item_number
        self.orderable = inventory_item.orderable
        self.quantity = quantity
