# Generated by Django 4.1.7 on 2023-03-22 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_favourites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favourites',
        ),
    ]
