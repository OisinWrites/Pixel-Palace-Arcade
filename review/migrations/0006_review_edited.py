# Generated by Django 3.2 on 2023-06-06 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_remove_review_aggregaterating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='edited',
            field=models.BooleanField(null=True),
        ),
    ]
