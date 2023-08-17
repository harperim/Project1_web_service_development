from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.utils import timezone

class Product(models.Model):
    theme_choices=[
            ('힐링', '힐링'),
            ('문화체험', '문화체험'),
            ('액티비티', '액티비티'), 
            ('역사 가이드', '역사 가이드'),
        ]
    
    personned_choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'), 
            (4, '4'),
            (5, '5'), 
            (6, '6'),
            (7, '7'),
            (8, '8'), 
            (9, '9'),
            (15, '10 or more'),
        ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    
    # image = models.ImageField(upload_to="", blank=False, null=False)
    
    country = CountryField(blank_label='select country')
    region = models.CharField(max_length=50, default=' ')
    theme = models.CharField(choices=theme_choices, max_length=30)
    max_personned = models.IntegerField(choices=personned_choices)
    
    # 찜하기
    wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wish_products')
    
class Review(models.Model):
    score_choices = [
        (1, '1'),
        (2, '2'), 
        (3, '3'),
        (4, '4'), 
        (5, '5'),
    ]
    content = models.CharField(max_length=200)
    
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
   
    score = models.IntegerField(choices=score_choices)
    date = models.DateTimeField(default=timezone.now)  # auto_now=True


class Proposal(models.Model):
    personned_choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'), 
            (4, '4'),
            (5, '5'), 
            (6, '6'),
            (7, '7'),
            (8, '8'), 
            (9, '9'),
            (15, '10 or more'),
        ]
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proposals')
    tour_date = models.DateField(default=timezone.now)  # auto_now=True
    personned = models.IntegerField(choices=personned_choices)
    comment = models.CharField(max_length=500)
    
    # 요청 수락
    accept = models.BooleanField()
    
    
# class Accept(models.Model):
    
#     writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accepts')
#     date = models.DateTimeField(default=timezone.now)  # auto_now=True