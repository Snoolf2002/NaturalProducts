# Generated by Django 4.0.4 on 2022-05-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_remove_order_payment_remove_orderlist_total_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderlist',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='orderlist',
            name='total_payment',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
