from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    USER_TYPES = (
        ('C', 'مشتری'),
        ('M', 'مکانیک'),
        ('F', 'شرکت')
    )

    type = models.CharField(max_length=1, choices=USER_TYPES, blank=True, null=True, default="C")  
    
    def __str__(self):
        return self.username