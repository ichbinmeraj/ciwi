from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.template.defaultfilters import slugify
from uuid import uuid4

class Category(models.Model):
    
    DELETED_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=150)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    created_at = jmodels.jDateTimeField(blank=True, null=True)
    updated_at = jmodels.jDateTimeField(blank=True, null=True)    
    is_deleted = models.CharField(max_length=1, choices=DELETED_CHOICES, blank=True, null=True, default="P")

    def __str__(self):
        return f"{self.name}"
               
    def save(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = 'N'
        
        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
        
        if not self.slug:
            self.slug = str(uuid4()).split('-')[4]

        self.slug = slugify('{}'.format(self.slug))
        self.updated_at = timezone.localtime(timezone.now())

        super(Category, self).save(*args, **kwargs)

class Item(models.Model):

    DELETED_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    ITEM_TYPES = (
        ('S', 'Service'),
        ('p', 'Product'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=150)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    type = models.CharField(max_length=1, choices=ITEM_TYPES, blank=True, null=True, default="P")
    price = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    category = models.ManyToManyField(Category)
    created_at = jmodels.jDateTimeField(blank=True, null=True)
    updated_at = jmodels.jDateTimeField(blank=True, null=True)    
    is_deleted = models.CharField(max_length=1, choices=DELETED_CHOICES, blank=True, null=True, default="N")

    def __str__(self):
        return f"{self.name} / ({self.price:,d})"
        
    def save(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = 'N'
        
        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
        
        if not self.slug:
            self.slug = str(uuid4()).split('-')[4]

        self.slug = slugify('{}'.format(self.slug))
        self.updated_at = timezone.localtime(timezone.now())

        super(Item, self).save(*args, **kwargs)
class Customer(models.Model):

    DELETED_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=150)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=50)
    address = models.TextField(blank=True, null=True)
    created_at = jmodels.jDateTimeField(blank=True, null=True)
    updated_at = jmodels.jDateTimeField(blank=True, null=True)
    is_deleted = models.CharField(max_length=1, choices=DELETED_CHOICES, blank=True, null=True, default="N")
    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): 
        if not self.is_deleted:
            self.is_deleted = 'N' 

        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
              
        if not self.slug:
            self.slug = str(uuid4()).split('-')[4]

        self.slug = slugify('{}'.format(self.slug))
        self.updated_at = timezone.localtime(timezone.now())

        super(Customer, self).save(*args, **kwargs)

class Invoice(models.Model):
    DELETED_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    INVOICE_TYPE = (
        ('W', 'فاکتور خدمات'),
        ('M', 'فاکتور فروش'),
    )

    STATUS_CHOICES = (
        ('c', 'پرداخت شده با کارت خوان'),
        ('n', 'پرداخت نقدی'),
        ('k', 'پرداخت کارت به کارت'),
        ('u', 'پرداخت نشده'),
    )    

    id = models.AutoField(primary_key=True)
    code = models.CharField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = jmodels.jDateTimeField(blank=True, null=True)
    updated_at = jmodels.jDateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='u')
    type = models.CharField(max_length=1, choices=INVOICE_TYPE, blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    items = models.ManyToManyField(Item)

    #related fields
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    decription = models.TextField(blank=True, null=True)
    is_deleted = models.CharField(max_length=1, choices=DELETED_CHOICES, blank=True, null=True, default="N")


    def __str__(self):
        return f'{self.code} {self.date}'


    def save(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = 'N'
        
        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
        
        if not self.slug:
            self.slug = str(uuid4()).split('-')[4]

        self.slug = slugify('{}'.format(self.slug))
        self.updated_at = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)   