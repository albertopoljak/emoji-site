# Generated by Django 3.2.3 on 2021-05-23 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emoji_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emoji',
            name='image',
            field=models.ImageField(upload_to='media/emotes'),
        ),
    ]