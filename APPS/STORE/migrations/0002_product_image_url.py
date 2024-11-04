# Generated by Django 4.2.14 on 2024-10-25 11:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='media/products'),
            preserve_default=False,
        ),
    ]
