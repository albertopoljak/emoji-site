# Generated by Django 5.0.3 on 2024-03-23 12:32

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatvibes_app", "0002_rename_userimagereports_userimagereport"),
    ]

    operations = [
        migrations.AddField(
            model_name="copyright",
            name="create_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AddField(
            model_name="copyright",
            name="date_create",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="copyright",
            name="date_write",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="copyright",
            name="write_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AddField(
            model_name="license",
            name="create_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AddField(
            model_name="license",
            name="date_create",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="license",
            name="date_write",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="license",
            name="write_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AddField(
            model_name="userimagereport",
            name="create_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AddField(
            model_name="userimagereport",
            name="date_create",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userimagereport",
            name="date_write",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userimagereport",
            name="write_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="create_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="write_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="imagecollection",
            name="create_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="imagecollection",
            name="write_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="chatvibes_app.userprofile",
            ),
        ),
    ]
