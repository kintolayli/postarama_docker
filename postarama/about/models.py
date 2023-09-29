from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="about/")


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True, null=True)
