# Generated by Django 3.2 on 2024-11-08 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20241108_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='image',
            field=models.URLField(blank=True, default='resources\\defaults/default_ingredient.jpg', null=True),
        ),
        migrations.AlterField(
            model_name='utensil',
            name='image',
            field=models.URLField(blank=True, default='resources\\defaults/default_utensil.jpg', null=True),
        ),
    ]