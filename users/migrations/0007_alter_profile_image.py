# Generated by Django 3.2.7 on 2022-04-27 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_is_activated_customuser_is_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_profile_picture.jpg', upload_to='profile_pics'),
        ),
    ]