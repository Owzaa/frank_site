# Generated by Django 4.2.14 on 2025-02-12 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='updated_at',
            new_name='published_at',
        ),
    ]
