# Generated by Django 3.2 on 2024-11-08 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220427_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipeimage',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='utensil',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
