# Generated by Django 5.0.3 on 2024-03-23 12:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chatvibes_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserImageReports",
            new_name="UserImageReport",
        ),
    ]
