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
    
    class Meta:
        ordering = ['-id']

    @property
    def total_payment(self):
        payments_sum = 0
        orders = self.list.all()
        # for order in orders:
        #     payments_sum += float(order.total_payment)
        # print(payments_sum)
        payments_sum=sum(orders.payment)
        return payments_sum

    def __str__(self) -> str:
        return f'{self.id} - buyurtma'