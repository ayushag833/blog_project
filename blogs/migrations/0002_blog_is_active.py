# Generated by Django 5.1.4 on 2025-01-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
