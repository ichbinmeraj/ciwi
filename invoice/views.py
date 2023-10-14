from django.shortcuts import render
from .models import Invoice, Customer, Item


def workshop(request):
    last_5_invoice = Invoice.objects.filter(is_deleted="N", type="W").order_by("-id")[:5]
    last_5_customer = Customer.objects.filter(is_deleted="N").order_by("-id")[:5]
    last_5_service = Item.objects.filter(is_deleted="N", type="S").order_by("-id")[:5]

    context = {
        "invoices":last_5_invoice,
        "customers":last_5_customer,
        "services":last_5_service,
    }

    return render(request, "workshop.html", context)

def mechanickala(request):
    last_5_invoice = Invoice.objects.filter(is_deleted="N", type="M").order_by("-id")[:5]
    last_5_customer = Customer.objects.filter(is_deleted="N").order_by("-id")[:5]
    last_5_product = Item.objects.filter(is_deleted="N", type="P").order_by("-id")[:5]

    context = {
        "invoices":last_5_invoice,
        "customers":last_5_customer,
        "products":last_5_product,
    }

    return render(request, "mechanickala.html", context)