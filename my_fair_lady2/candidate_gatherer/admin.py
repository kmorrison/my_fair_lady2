from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.SourceType)
admin.site.register(models.Source)
admin.site.register(models.Candidate)
