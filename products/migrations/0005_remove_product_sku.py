# Generated by Django 3.2 on 2023-04-17 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_has_variants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
    ]