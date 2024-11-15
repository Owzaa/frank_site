# Generated by Django 4.2.14 on 2024-10-30 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SliderImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_title', models.CharField(blank=True, max_length=100)),
                ('img_slide', models.ImageField(upload_to='media/projects/slider_images')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project_start', models.DateTimeField()),
                ('project_finished', models.DateTimeField()),
                ('description', models.TextField()),
                ('technology', models.CharField(max_length=50)),
                ('project_url', models.URLField()),
                ('project_logo', models.ImageField(upload_to='media/projects')),
                ('project_slide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Portfolio.sliderimages')),
            ],
        ),
    ]
