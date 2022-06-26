from django.db import models
from shop.models.product import Product


class Order(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount      = models.IntegerField(default=1)
    user        = models.ForeignKey('users.MyUser', on_delete=models.CASCADE)

    @property
    def payment(self):
        return self.product.price*self.amount
    
    def __str__(self) -> str:
        return f'{self.product}'


class OrderList(models.Model):
    list            = models.ManyToManyField(Order)
    order_time      = models.DateTimeField(auto_now_add=True)
    user            = models.ForeignKey('users.MyUser', on_delete=models.CASCADE)
    total_payment   = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f'{self.id} - buyurtma'