# Generated by Django 3.2 on 2023-06-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20230606_0826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='user_rating',
        ),
        migrations.AddField(
            model_name='rating',
            name='rating',
            field=models.PositiveIntegerField(choices=[
                (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
    ]
