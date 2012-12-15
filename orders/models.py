from django.db import models

from inventory.models import Label, InventoryItemLink

class Order(models.Model):
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description

    def generate_labels(self):
        labels = []
        for order_item in self.orderitem_set.all():
            inventory_item = order_item.inventory_item
            labels.extend(
                self.generate_labels_for_quantity(
                    inventory_item,
                    order_item.quantity,
                    relationship = None
                )
            )
            labels.extend(
                self.generate_labels_for_children(inventory_item)
            )

        return labels

    def generate_labels_for_children(self, inventory_item):
        labels = []
        for inventory_item_link in InventoryItemLink.objects.filter(
            parent_inventory_item = inventory_item):
            labels.extend(
                self.generate_labels_for_quantity(
                    inventory_item_link.child_inventory_item,
                    inventory_item_link.num_child_inventory_items_required,
                    inventory_item_link.relationship
                )
            )
            labels.extend(
                self.generate_labels_for_children(
                    inventory_item_link.child_inventory_item
                )
            )
        return labels

    def generate_labels_for_quantity(self, inventory_item, quantity, relationship):
        labels = []
        num_left = quantity
        while num_left > 0:
            label = Label(
                inventory_item,
                min(num_left, inventory_item.max_per_container),
                relationship
            )
            labels.append(label)
            num_left -= inventory_item.max_per_container
        return labels


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    inventory_item = models.ForeignKey(
        "inventory.InventoryItem",
        limit_choices_to = {'orderable': True}
    )
    quantity = models.IntegerField()

    def __unicode__(self):
        return "%s %s%s" % (
            self.quantity,
            self.inventory_item,
            's' if self.quantity > 1 else ''
        )
