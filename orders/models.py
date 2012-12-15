from django.db import models

from inventory.models import Label, InventoryItemLink

class Order(models.Model):
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description

    def generate_labels(self):
        """
        Generates a alpabetically sorted list of labels for each item
        that is required for this order, including all child items.
        """
        items_for_order = self._generate_items_for_order()
        labels = []
        for item, relationship_to_quantity_mapping in items_for_order.iteritems():
            for relationship, quantity in relationship_to_quantity_mapping.iteritems():
                while quantity > 0:
                    label_quantity = min(quantity, item.max_per_container)
                    labels.append(Label(item, relationship, label_quantity))
                    quantity -= label_quantity

        labels = sorted(labels, key=lambda label: label.name)
        return labels
        
    def _generate_items_for_order(self):
        """
        Will generate a dict with totals of all items required for the
        order, refined by the relationship. The resulting dict format is:
            
        items_for_order = {
                item1: {
                    relationshipA: quantity,
                    relationshipB: quantity
                },
                item2: {
                    relationshipC: quantity,
                    relationshipD: quantity
                }
            }
        """
        items_for_order = {}
        for order_item in self.orderitem_set.all():
            inventory_item = order_item.inventory_item
            if not inventory_item in items_for_order.keys():
                items_for_order[inventory_item] = {
                    '': order_item.quantity
                }
            else:
                items_for_order[inventory_item][''] += order_item.quantity

            self._generate_items_for_item_children(
                parent_item = inventory_item, 
                quantity_of_parent_item = order_item.quantity, 
                items_for_order = items_for_order
            )

        return items_for_order

    def _generate_items_for_item_children(self, parent_item, quantity_of_parent_item, items_for_order):
        """
        Helper for _generate_items_for_order that will recursively
        add to the items_for_order dict for all child items, and their
        child items, and so on.
        """
        for item_link in InventoryItemLink.objects.filter(
            
            parent_inventory_item = parent_item):
            child_item = item_link.child_inventory_item
            num_child_items = quantity_of_parent_item * item_link.num_child_inventory_items_required
            relationship = item_link.relationship

            if child_item not in items_for_order:
                items_for_order[child_item] = {}
            if relationship not in items_for_order[child_item]:
                items_for_order[child_item][relationship] = num_child_items
            else:
                items_for_order[child_item][relationship] += num_child_items 

            self._generate_items_for_item_children(
                parent_item = child_item,
                quantity_of_parent_item = num_child_items,
                items_for_order = items_for_order
            )


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
