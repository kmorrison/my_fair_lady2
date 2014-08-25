from django.contrib import admin
from django.db import models


class SourceType(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s%s" % (self.name, " (Is Active)" if self.is_active else "")


class Source(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, verbose_name="Source Name")

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


def recent_sources():
    recent_sources_to_show = 5
    active_source_types = SourceType.objects(
        is_active=True,
    ).all()

    if not active_sources_types:
        return []
    return Source.objects.filter(
        source_type_id=active_source_types[0].id,
    ).order_by(
        '-time_created',
    ).all()[:recent_sources_to_show]
