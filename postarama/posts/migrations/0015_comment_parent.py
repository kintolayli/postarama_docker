# Generated by Django 2.2.6 on 2020-12-11 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0014_auto_20201209_0148"),
    ]

    operations = [
        migrations.AddField(
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
