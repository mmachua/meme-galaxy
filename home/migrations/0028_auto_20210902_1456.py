# Generated by Django 3.2 on 2021-09-02 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_post_image4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image1',
            field=models.ImageField(null=True, upload_to='posts/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image4',
            field=models.ImageField(blank=True, upload_to='posts/%Y/%m/%d'),
        ),
    ]
