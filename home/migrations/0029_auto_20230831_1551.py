# Generated by Django 3.2 on 2023-08-31 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20210902_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image4',
        ),
    ]
