# Generated by Django 3.2 on 2023-07-20 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_alter_userprofile_newsletter_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='newsletter_subscribed',
        ),
    ]