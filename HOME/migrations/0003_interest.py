# Generated by Django 4.2.14 on 2025-02-07 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HOME', '0002_rename_client_slide_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_name', models.CharField(max_length=100)),
                ('interest_icon', models.ImageField(upload_to='media/interests')),
            ],
        ),
    ]
