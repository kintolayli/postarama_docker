# Generated by Django 2.2.6 on 2020-11-22 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("likes", "0003_auto_20201123_0052"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="contenttypes.ContentType",
            ),
        ),
    ]
