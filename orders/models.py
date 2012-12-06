from django.db import models

class Order(models.Model):
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description

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
