from django.contrib import admin
from .models import Invoice, Item, Category, Customer, InvoiceDetail

admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(InvoiceDetail)
admin.site.register(Customer)