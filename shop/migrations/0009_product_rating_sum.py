# Generated by Django 4.0.4 on 2022-05-05 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_rating_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating_sum',
            field=models.FloatField(blank=True, default=5, null=True),
        ),
    ]
