# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RawFeed'
        db.create_table(u'neo_core_rawfeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('item_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('feed_type', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'neo_core', ['RawFeed'])


    def backwards(self, orm):
        # Deleting model 'RawFeed'
        db.delete_table(u'neo_core_rawfeed')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'neo_core.rawfeed': {
            'Meta': {'object_name': 'RawFeed'},
            'feed_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'item_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['neo_core']