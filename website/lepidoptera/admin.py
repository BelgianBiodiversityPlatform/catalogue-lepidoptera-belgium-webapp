from django.contrib import admin
from .models import Family


class FamilyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Family, FamilyAdmin)
