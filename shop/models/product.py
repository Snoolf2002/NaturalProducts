from django.db import models

from shop.models.catagory import Catagory


class Product(models.Model):

    PRICE_TYPE = [
        ('dona', 'one'),
        ('quti', 'box'),
        ('kilogramm', 'kilogram')
    ]

    catagory        = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    title           = models.CharField(max_length=63, null=False)
    image           = models.ImageField(null=False, blank=False, upload_to='products/')
    price           = models.FloatField(null=False, blank=False)
    price_type      = models.CharField(choices=PRICE_TYPE, max_length=10, null=False, default='kilogram')
    descreption     = models.CharField(max_length=255, null=True, blank=False)
    rating          = models.FloatField(null=False, default=5)
    rating_amount   = models.IntegerField(null=True, blank=True, default=1)
    rating_sum      = models.FloatField(null=True, blank=True, default=5)
    is_favorite     = models.BooleanField(default=False)
    order_amount    = models.IntegerField(default=0, blank=False, null=False)
    
    def __str__(self) -> str:
        return self.title

