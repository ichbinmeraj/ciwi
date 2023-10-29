from django import forms
from django.forms import formset_factory
from .models import Invoice, Customer, Item, Category, InvoiceDetail

class ProductForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'qty', 'type', 'category']
        
        labels = {
            'name':'نام کالا',
            'price':'قیمت',
            'qty':'تعداد اولیه',
        }
    type = forms.ChoiceField(
        choices=[('S', 'Service'), ('P', 'Product')],
        initial='P',
        widget=forms.HiddenInput(),
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(is_deleted="N"),
        widget=forms.CheckboxSelectMultiple,
        label="دسته بندی ها :",
        required=False
    )

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'type']

        labels = {
            'name':'عنوان',
            'price':'هزینه',
        }
    type = forms.ChoiceField(
        choices=[('S', 'Service'), ('P', 'Product')],
        initial='S',
        widget=forms.HiddenInput(),
    )

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address']
    name = forms.CharField(label="اسم")
    phone = forms.IntegerField(label="شماره تلفن")
    address = forms.CharField(widget=forms.Textarea, label="آدرس")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name':'عنوان',
        }

class InvoiceMechanickalaForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['code', 'status', 'customer', 'date']
        

        labels = {
            'status':'وضعیت پرداخت',
            'customer':'مشتری',
        }

    date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1401-01-01'}),label="تاریخ")
    code = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}),label="کد فاکتور", required=False)


class InvoiceMechanickalaDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'invoice' in kwargs and 'item' in kwargs and 'amount' in kwargs:
            self.invoice = kwargs.pop('invoice')
            self.item = kwargs.pop('item')
            self.amount = kwargs.pop('amount')
        super().__init__(*args, **kwargs)

    class Meta:
        model = InvoiceDetail
        fields = [
            'invoice',
            'item',
            'amount',   
        ]
        widgets = {
            'item': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_product',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_amount',
                'placeholder': '0',
                'type': 'number',
            })
        }

InvoiceDetailFormSet = formset_factory(InvoiceMechanickalaDetailForm, extra=1)