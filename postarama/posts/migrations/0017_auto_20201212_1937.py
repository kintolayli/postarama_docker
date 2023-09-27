# Generated by Django 2.2.6 on 2020-12-12 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0016_auto_20201212_0159"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="parent_comment",
                to="posts.Comment",
                verbose_name="parent comment",
            ),
        ),
    ]
