# Generated by Django 2.2.6 on 2020-11-22 22:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("likes", "0004_auto_20201123_0106"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.ContentType",
            ),
        ),
    ]
