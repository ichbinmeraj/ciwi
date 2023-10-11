from django.contrib import admin
from .models import Invoice, Customer, Mechanic

admin.site.register(Invoice)
admin.site.register(Customer)
admin.site.register(Mechanic)