from django.db import models


class Family(models.Model):
    family_id = models.IntegerField(unique=True)  # ID from the Access database, not Django's PK
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "families"