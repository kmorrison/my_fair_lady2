from django.contrib import admin

from . import models

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_created', 'number_of_candidates')


class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'email_address', 
        'time_created', 
        'source',
    )

    list_filter = (
        'source__name',
    )


# Register your models here.
admin.site.register(models.SourceType)
admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Candidate, CandidateAdmin)
