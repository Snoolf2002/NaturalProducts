from django.db import models


class Catagory(models.Model):

    CATAGORY = [
        ('Fruit', 'fruit'),
        ('Vegetable', 'vegetable'),
        ('Greens', 'greens'),
        ('Spices', 'spices')
    ]

    title       = models.CharField(choices=CATAGORY, max_length=10, null=False, default='fruit')
    image       = models.ImageField(upload_to='catagory/', blank=False)
    descreption = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.title