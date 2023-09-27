# Generated by Django 2.2.6 on 2020-12-08 22:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0013_auto_20201209_0147"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupfollow",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="group_follower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
