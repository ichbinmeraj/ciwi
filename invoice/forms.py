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

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['code', 'status', 'customer', 'date', 'type', 'discountprice']
        

        labels = {
            'status':'وضعیت پرداخت',
            'customer':'مشتری',
            'discountprice':'تخفیف',
        }
    
    type = forms.ChoiceField(
        choices=[('W', 'فاکتور خدمات'),
        ('M', 'فاکتور فروش')],
        initial='W',
        widget=forms.HiddenInput(),
    )    

    date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1401-01-01'}),label="تاریخ")
    code = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}),label="کد فاکتور", required=False)


class InvoiceMechanickalaDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = [
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

    def __init__(self, *args, **kwargs):
        super(InvoiceMechanickalaDetailForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(type='P', is_deleted='N')

InvoiceMechanickalaDetailFormSet = formset_factory(InvoiceMechanickalaDetailForm, extra=1)


class InvoiceWorkshopDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = [
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

    def __init__(self, *args, **kwargs):
        super(InvoiceWorkshopDetailForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(type='S', is_deleted='N')

InvoiceWorkshopDetailFormSet = formset_factory(InvoiceWorkshopDetailForm, extra=1)