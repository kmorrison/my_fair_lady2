from django.contrib import admin
from django.db import models

class SourceType(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Source(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)

    source_type = models.ForeignKey(
        SourceType,
    )

    def __unicode__(self):
        return self.name


class Candidate(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.EmailField()

    phone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    source = models.ForeignKey(
        Source,
    )

    def __unicode__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.email_address)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name, )


admin.site.register(SourceType)
admin.site.register(Source)
admin.site.register(Candidate)
