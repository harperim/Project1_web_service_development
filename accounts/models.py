from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

from django.utils import timezone

class User(AbstractUser):
    group_choices=[
            ('tourist', '투어리스트'),
            ('guide', '가이드'),
        ]
    
    guides = models.ManyToManyField('self', symmetrical=False, related_name='tourists', blank=False)
    
    
    group = models.CharField(choices=group_choices, max_length=10)
    email = models.EmailField(
        max_length=100, 
        null=False,
        unique=True, 
        blank=True
        )
    phone = models.CharField(max_length=11)
    country = CountryField(blank_label='select country', default=' ')
    city = models.CharField(max_length=50, default=' ')
    language = models.CharField(max_length=20, default=' ')
    is_guide = models.BooleanField(default=False)
    is_tourist = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    

    