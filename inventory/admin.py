from inventory.models import InventoryItem, InventoryItemLink
from django.contrib import admin

class InventoryItemLinkInline(admin.StackedInline):
    model = InventoryItemLink
    fk_name = "parent_inventory_item"
    extra = 1

class InventoryItemAdmin(admin.ModelAdmin):
    inlines = [InventoryItemLinkInline]
    list_display = ('name', 'description', 'orderable')
    search_fields = ['name', 'description']

admin.site.register(InventoryItem, InventoryItemAdmin)
