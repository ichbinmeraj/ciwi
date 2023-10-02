from django.db import models
from django_jalali.db import models as jmodels

class Invoice(models.Model):

    DELETED_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    STATUS_CHOICES = (
        ('c', 'پرداخت شده با کارت خوان'),
        ('n', 'پرداخت نقدی'),
        ('k', 'پرداخت کارت به کارت'),
        ('u', 'پرداخت نشده'),
    )    

    id = models.AutoField(primary_key=True)
    code = models.CharField(blank=True, null=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    created_at = jmodels.jDateTimeField(blank=True, null=True)
    updated_at = jmodels.jDateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='u')
    date = jmodels.jDateField(blank=True, null=True)
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

        super(Service, self).save(*args, **kwargs)   