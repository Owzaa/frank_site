# Generated by Django 4.2.14 on 2024-10-25 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_alter_product_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.ImageField(upload_to='media/products'),
        ),
    ]
