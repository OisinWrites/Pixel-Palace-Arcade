# Generated by Django 3.2 on 2023-07-20 21:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration', '0003_newslettersubscriber'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewsletterSubscriber',
            new_name='Subscriber',
        ),
    ]
