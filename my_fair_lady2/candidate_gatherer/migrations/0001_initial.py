# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SourceType'
        db.create_table(u'candidate_gatherer_sourcetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'candidate_gatherer', ['SourceType'])

        # Adding model 'Source'
        db.create_table(u'candidate_gatherer_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('source_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['candidate_gatherer.SourceType'])),
        ))
        db.send_create_signal(u'candidate_gatherer', ['Source'])

        # Adding model 'Candidate'
        db.create_table(u'candidate_gatherer_candidate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['candidate_gatherer.Source'])),
        ))
        db.send_create_signal(u'candidate_gatherer', ['Candidate'])


    def backwards(self, orm):
        # Deleting model 'SourceType'
        db.delete_table(u'candidate_gatherer_sourcetype')

        # Deleting model 'Source'
        db.delete_table(u'candidate_gatherer_source')

        # Deleting model 'Candidate'
        db.delete_table(u'candidate_gatherer_candidate')


    models = {
        u'candidate_gatherer.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['candidate_gatherer.Source']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'candidate_gatherer.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['candidate_gatherer.SourceType']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'candidate_gatherer.sourcetype': {
            'Meta': {'object_name': 'SourceType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['candidate_gatherer']