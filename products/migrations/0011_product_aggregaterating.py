# Generated by Django 3.2 on 2023-06-06 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_product_aggregaterating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='aggregaterating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
