# Generated by Django 2.2.6 on 2020-11-22 13:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_auto_20201122_1611"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Like",
        ),
    ]
