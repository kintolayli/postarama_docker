# Generated by Django 2.2.6 on 2020-11-23 17:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0009_remove_comment_text2"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-updated"]},
        ),
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[("draft", "Draft"), ("published", "Published")],
                default="draft",
                max_length=10,
            ),
        ),
    ]
