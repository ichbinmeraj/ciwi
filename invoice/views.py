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

from django.db.models import Q

def lists(request, page):

    obj = {
        "invoice-workshop": ["bi-receipt", "فاکتور های خدمات"],
        "invoice-mechanickala": ["bi-receipt", "فاکتور های فروش"],
        "products": ["bi-box-seam-fill", "لیست کالا ها"],
        "services": ["bi-database-fill-gear", "لیست خدمات"],
        "customer-workshop": ["bi-person-fill", "لیست مشتری های کارگاه تراشکاری"],
        "customer-mechanickala": ["bi-person-fill", "لیست مشتری های مکانیک کالا"],
    }
    
    context = {
        "context": Invoice.objects.filter(is_deleted="N", type="W").order_by("-id") if page == "invoice-workshop"
        else 
        Invoice.objects.filter(is_deleted="N", type="M").order_by("-id") if page == "invoice-mechanickala"
        else 
        Item.objects.filter(is_deleted="N", type="P").order_by("-id") if page == "products"
        else 
        Item.objects.filter(is_deleted="N", type="S").order_by("-id") if page == "services"
        else 
        Customer.objects.filter(is_deleted="N", invoice__type="W").order_by("-id") if page == "customer-workshop"
        else 
        Customer.objects.filter(is_deleted="N", invoice__type="M").order_by("-id") if page == "customer-mechanickala"
        else None,

        "page": page,
        "icon": obj[page][0],
        "name": obj[page][1],
    }

    return render(request, "lists.html", context)