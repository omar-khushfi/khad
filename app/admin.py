from django.contrib import admin
from .models import *

class OrderItemInline(admin.TabularInline):
    model = product_in_order
    extra = 1
    fields = ('product', 'quantity', 'subtotal')
    readonly_fields = ('subtotal',)

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)  # Save items first

        # Update the total price for the order after adding or modifying an item
        order = form.instance  # Represents the order
        total = 0  # Variable to hold the total price

        # Calculate the total price
        for item in order.product_in_order_set.all():  # Use related_name if defined
            total += item.subtotal()  # Use the subtotal method
           

        order.total = total  # Update the total price of the order
        order.save()  # Save the order with the updated total price
       

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('name', 'total', 'email', 'phone_number', 'date')
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.update_order_total(obj)

    def update_order_total(self, order):
        total = sum(item.subtotal() for item in order.product_in_order_set.all())
        order.total = total
        order.save()

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(product_in_order)
