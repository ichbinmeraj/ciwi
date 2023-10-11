from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    USER_TYPES = (
        ('C', 'مشتری'),
        ('M', 'مکانیک'),
        ('F', 'شرکت')
    )

    type = models.CharField(max_length=1, choices=USER_TYPES, blank=True, null=True, default="C") 
    phone = models.IntegerField(null=True, blank=True)
    address = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.username}({self.get_type_display()})' #this shit get 2 hours of my time :)
       