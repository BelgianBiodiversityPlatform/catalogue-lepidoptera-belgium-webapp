from django.db import models


class Family(models.Model):
    family_id = models.IntegerField(unique=True)  # ID from the Access database, not Django's PK
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "families"


class Species(models.Model):
    name = models.CharField(max_length=255)


class Province(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)


class TimePeriod(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField()


class SpeciesPresence(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE)