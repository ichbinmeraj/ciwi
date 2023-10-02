from django.db import models
from django_jalali.db import models as jmodels

class Inventory(models.Model):

    DELETED_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    decription = models.TextField(blank=True, null=True)
    created_at = jmodels.jDateTimeField(blank=True, null=True)
    updated_at = jmodels.jDateTimeField(blank=True, null=True)
    is_deleted = models.CharField(max_length=1, choices=DELETED_CHOICES, blank=True, null=True, default="N")


    def __str__(self):
        return f'{self.name}'


    def save(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = 'N'
        
        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
        
        if not self.slug:
            self.slug = str(uuid4()).split('-')[4]

        self.slug = slugify('{}'.format(self.slug))
        self.updated_at = timezone.localtime(timezone.now())

        super(Inventory, self).save(*args, **kwargs)

class Item(models.Model):

    DELETED_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    ITEM_TYPES = (
        ('S', 'Service'),
        ('p', 'Product')
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=150)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    type = models.CharField(max_length=1, choices=ITEM_TYPES, blank=True, null=True, default="N")
    price = models.IntegerField(blank=True, null=True)
    created_at = jmodels.jDateTimeField(blank=True, null=True)
    updated_at = jmodels.jDateTimeField(blank=True, null=True)    
    is_deleted = models.CharField(max_length=1, choices=DELETED_CHOICES, blank=True, null=True, default="P")

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

        super(Service, self).save(*args, **kwargs)


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
    