from orders.models import Order, OrderItem
from django.contrib import admin

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    fk_name = "order"
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['description']
    search_fields = ['description']

admin.site.register(Order, OrderAdmin)
