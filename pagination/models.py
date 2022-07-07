from django.db import models


class Text(models.Model):
    description = models.CharField(max_length=50)
