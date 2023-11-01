from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, Customer, Item, Category, InvoiceDetail
from .forms import ServiceForm, ProductForm, CustomerForm, CategoryForm, InvoiceForm, InvoiceMechanickalaDetailForm, InvoiceMechanickalaDetailFormSet, InvoiceWorkshopDetailForm, InvoiceWorkshopDetailFormSet
from django.contrib import messages


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
    last_5_category = Category.objects.filter(is_deleted="N").order_by("-id")[:5]

    context = {
        "invoices":last_5_invoice,
        "customers":last_5_customer,
        "products":last_5_product,
        "categories":last_5_category,
    }

    return render(request, "mechanickala.html", context)

# from django.db.models import Q

def lists(request, page):

    obj = {
        "invoice-workshop": ["bi-receipt", "فاکتور های خدمات"],
        "invoice-mechanickala": ["bi-receipt", "فاکتور های فروش"],
        "products": ["bi-box-seam-fill", "لیست کالا ها"],
        "services": ["bi-database-fill-gear", "لیست خدمات"],
        "customer-workshop": ["bi-person-fill", "لیست مشتری های کارگاه تراشکاری"],
        "customer-mechanickala": ["bi-person-fill", "لیست مشتری های مکانیک کالا"],
        "categories": ["bi-bookmark-check", "لیست دسته بندی ها"],
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
        else
        Category.objects.filter(is_deleted="N").order_by("-id") if page == "categories"
        else None,

        "page": page,
        "icon": obj[page][0],
        "name": obj[page][1],
    }
    
    
    return render(request, "lists.html", context)
# invoice imcomplete
def create(request, page):
    obj = {
        # "invoice-workshop": ["bi-receipt"],
        # "invoice-mechanickala": ["bi-receipt"],
        "products": ["bi-box-seam-fill"],
        "services": ["bi-database-fill-gear"],
        "customers": ["bi-person-fill"],
        "categories": ["bi-bookmark-check"],
    }
    form = (
            ServiceForm(request.POST or None)
            if page == "services"
            else ProductForm(request.POST or None)
            if page == "products"
            else CustomerForm(request.POST or None)
            if page  == "customers"
            else CategoryForm(request.POST or None)
            if page  == "categories"
            else None
        )

    if form.is_valid():
        form.save()
        messages.success(request, "The post has been updated successfully.")
        return redirect("home")
    else:
        messages.error(request, "Please correct the following errors:")
        return render(
            request, "details.html", {"form": form, "page": page, "icon": obj[page][0]}
        )



def create_invoice(request, page):
    value = {
        "mechanickala": ["اضافه کردن محصول دیگر"],
        "workshop": ["اضافه کردن خدمات دیگر"],
    }
    form = InvoiceForm()
    formset = InvoiceMechanickalaDetailFormSet() if page == "mechanickala" else InvoiceWorkshopDetailFormSet() if page == "workshop" else None
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceMechanickalaDetailFormSet(request.POST) if page == "mechanickala" else InvoiceWorkshopDetailFormSet(request.POST) if page == "workshop" else None    
        if form.is_valid():
            invoice = Invoice.objects.create(
                code=form.cleaned_data.get("code"),
                date=form.cleaned_data.get("date"),
                status=form.cleaned_data.get("status"),
                customer=form.cleaned_data.get("customer"),
            )
            if formset.is_valid():
                total = 0
                for form in formset:
                    item = form.cleaned_data.get("item")
                    amount = form.cleaned_data.get("amount")
                    if item and amount:
                        # Sum each row
                        sum = int(item.price) * int(amount)
                        # Sum of total invoice
                        total += sum
                        InvoiceDetail(invoice=invoice, item=item, amount=amount).save()
                # Save the invoice
                invoice.type = "M" if page == "mechanickala" else "W" if page == "workshop" else None 
                invoice.prices = total
                invoice.save()
                return redirect("home")

    context = {
        "form": form,
        "formset": formset,
        "value": value[page][0],
    }

    return render(request, "invoice/create_invoice.html", context)

# def details(request, page, id):

#     detail = get_object_or_404(
#         Invoice
#         if page == "invoice-workshop" or page == "invoice-mechanickala"
#         else Customer
#         if page == "customer-workshop" or page == "customer-mechanickala"
#         else Item
#         if page == "services" or page == "products"
#         else None,
#         id=id,
#     )
    
#     obj = {
#         "invoice-workshop": ["bi-receipt", "فاکتور های خدمات"],
#         "invoice-mechanickala": ["bi-receipt", "فاکتور های فروش"],
#         "products": ["bi-box-seam-fill", "لیست کالا ها"],
#         "services": ["bi-database-fill-gear", "لیست خدمات"],
#         "customer-workshop": ["bi-person-fill", "لیست مشتری های کارگاه تراشکاری"],
#         "customer-mechanickala": ["bi-person-fill", "لیست مشتری های مکانیک کالا"],
#     }

#     context = {"page": page,"icon": obj[page][0], "id": id}

#     if request.method == "GET":
#         context.update(
#             {
#                 "form": MechanicForm(instance=detail)
#                 if page == "mechanic"
#                 else CustomerForm(instance=detail)
#                 if page == "customer"
#                 else ServiceForm(instance=detail)
#                 if page == "service"
#                 else InvoiceForm(instance=detail)
#             }
#             )
        

#         return render(request, "details.html", context)

#     elif request.method == "POST":
#         form = (
#             MechanicForm(request.POST, instance=detail)
#             if page == "mechanic"
#             else CustomerForm(request.POST, instance=detail)
#             if page == "customer"
#             else ServiceForm(request.POST, instance=detail)
#             if page == "service"
#             else InvoiceForm(request.POST, instance=detail)
#         )
#         if form.is_valid():
#             form.save()
#             messages.success(request, "The post has been updated successfully.")
#             return redirect("main")
#         else:
#             messages.error(request, "Please correct the following errors:")
#             return render(
#                 request, "details.html", {"form": form, "page": page, "id": id}
#             )

def invoice_pdf(request, id):

    invoice = Invoice.objects.get(id=id)

    prices = 0 
    for service in invoice.services.values('price'):
        prices += service['price']
    
    taxprice = int(prices/100*9)

    finalprice = (prices)+(taxprice)
    
    context = {
        "invoice":invoice,
        "prices":prices,
        "taxprice":taxprice,
        "finalprice":finalprice,
    }
    return render(request, "invoice_pdf.html", context)