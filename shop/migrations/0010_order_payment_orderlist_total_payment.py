# Generated by Django 4.0.4 on 2022-05-06 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_product_rating_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='total_payment',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
