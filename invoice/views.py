from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Invoice, Customer, Item, Category, InvoiceDetail
from .forms import ServiceForm, ProductForm, CustomerForm, CategoryForm, InvoiceForm, InvoiceMechanickalaDetailForm, InvoiceMechanickalaDetailFormSet, InvoiceWorkshopDetailForm, InvoiceWorkshopDetailFormSet
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def workshop(request):
    if request.user.type != "W":
        messages.error(request, "شما اجازه این عملیات را ندارید!")
        return redirect('home')
    last_5_invoice = Invoice.objects.filter(is_deleted="N", type="W").order_by("-id")[:5]
    last_5_customer = Customer.objects.filter(is_deleted="N").order_by("-id")[:5]
    last_5_service = Item.objects.filter(is_deleted="N", type="S").order_by("-id")[:5]
    

    context = {
        "invoices":last_5_invoice,
        "customers":last_5_customer,
        "services":last_5_service,
    }

    return render(request, "workshop.html", context)

@login_required
def mechanickala(request):
    if request.user.type != 'K':
        messages.error(request, "شما اجازه این عملیات را ندارید!")
        return redirect('home')
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
@login_required
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

@login_required
def create(request, page):
    obj = {
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
        messages.success(request, " با موفقیت انجام شد!")
        return redirect("home")
    else:
        messages.error(request, "Please correct the following errors:")
        return render(
            request, "details.html", {"form": form, "page": page, "icon": obj[page][0]}
        )


@login_required
def create_invoice(request, page):
    value = {
        "mechanickala": ["کالا"],
        "workshop": ["خدمات"],
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
                messages.success(request, "فاکتور با موفقیت ایجاد شد!")
                return redirect(f"{page}")

    context = {
        "form": form,
        "formset": formset,
        "value": value[page][0],
    }

    return render(request, "invoice/create_invoice.html", context)

@login_required
def detail_invoice(request, page, id):
    value = {
        "mechanickala": ["لوازم یدکی مکانیک کالا"],
        "workshop": ["کارگاه تراشکاری شهرود سفری"],
    }
    obj = get_object_or_404(Invoice, id=id)
    form = InvoiceForm(request.POST or None, instance=obj)
    invoice = Invoice.objects.get(id=id)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    prices = invoice.prices
    taxprice = int(prices/100*9)
    discountprice = invoice.discountprice
    finalprice = (prices)+(taxprice)-(discountprice)

    if form.is_valid():
        form.save()
        return redirect(f'{page}')
    
    context = {
        "form": form,
        "invoice":invoice,
        "prices":prices,
        "taxprice":taxprice,
        "finalprice":finalprice,
        "discountprice":discountprice,
        "invoice_detail":invoice_detail,
        "value": value[page][0],
    }
    
    return render(request, "invoice/detail_invoice.html", context)

@login_required
def print_invoice(request, page, id):
    value = {
        "mechanickala": ["لوازم یدکی مکانیک کالا"],
        "workshop": ["کارگاه تراشکاری شهرود سفری"],
    }
    invoice = Invoice.objects.get(id=id)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    prices = invoice.prices
    taxprice = int(prices/100*9)
    discountprice = invoice.discountprice
    finalprice = (prices)+(taxprice)-(discountprice)
    
    context = {
        "invoice":invoice,
        "prices":prices,
        "taxprice":taxprice,
        "discountprice":discountprice,
        "finalprice":finalprice,
        "invoice_detail":invoice_detail,
        "value": value[page][0],
    }
    return render(request, "invoice/print_invoice.html", context)

@login_required
def details(request, page, id):

    detail = get_object_or_404(
        Customer
        if page == "customers"
        else Item
        if page == "services" or page == "products"
        else Category
        if page == "categories"
        else None,
        id=id,
    )
    
    obj = {
        "products": ["bi-box-seam-fill", "کالا ها"],
        "services": ["bi-database-fill-gear", "خدمات"],
        "categories": ["bi-bookmark-check", "دسته بندی ها"],
        "customers": ["bi-person-fill", "مشتری ها"],
    }

    context = {"page": page,"icon": obj[page][0], "id": id}

    if request.method == "GET":
        context.update(
            {
                "form": CustomerForm(instance=detail)
                if page == "customers"
                else ProductForm(instance=detail)
                if page == "products"
                else ServiceForm(instance=detail)
                if page == "services"
                else CategoryForm(instance=detail)
                if page == "categories"
                else None
            }
            )
        

        return render(request, "details.html", context)

    elif request.method == "POST":
        form = (
            CustomerForm(request.POST, instance=detail)
            if page == "customers"
            else ProductForm(request.POST, instance=detail)
            if page == "products"
            else ServiceForm(request.POST, instance=detail)
            if page == "services"
            else CategoryForm(request.POST, instance=detail)
            if page == "categories"
            else None
        )
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been updated successfully.")
            return redirect("lists", page=page)
        else:
            messages.error(request, "Please correct the following errors:")
            return render(
                request, "details.html", {"form": form, "page": page, "id": id}
            )




@login_required
def deactive_invoice(request, page, id):
    invoice = Invoice.objects.get(id=id)
    invoice.is_deleted = "Y"
    invoice.save()
    messages.success(request, " با موفقیت حذف شد!")
    return redirect("lists", page=page)

@login_required
def deactive(request, page, id):
    obj = ( Customer.objects.get(id=id)
    if page == "customers"
    else Item.objects.get(id=id)
    if page == "services" or page == "products"
    else Category.objects.get(id=id)
    if page == "categories"
    else None)
    obj.is_deleted = "Y"
    obj.save()
    messages.success(request, " با موفقیت حذف شد!")
    return redirect(f"../../lists/{page}")