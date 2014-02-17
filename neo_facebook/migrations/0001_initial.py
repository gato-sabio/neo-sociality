# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Newsmaker'
        db.create_table(u'neo_facebook_newsmaker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('about', self.gf('django.db.models.fields.TextField')(null=True)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'neo_facebook', ['Newsmaker'])

        # Adding model 'Post'
        db.create_table(u'neo_facebook_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['neo_facebook.Newsmaker'])),
            ('fb_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('header', self.gf('django.db.models.fields.TextField')(default='', null=True)),
            ('message', self.gf('django.db.models.fields.TextField')(default='')),
            ('link', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 2, 0, 0))),
            ('post_type', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('like_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('repost_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'neo_facebook', ['Post'])


    def backwards(self, orm):
        # Deleting model 'Newsmaker'
        db.delete_table(u'neo_facebook_newsmaker')

        # Deleting model 'Post'
        db.delete_table(u'neo_facebook_post')


    models = {
        u'neo_facebook.newsmaker': {
            'Meta': {'object_name': 'Newsmaker'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'neo_facebook.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['neo_facebook.Newsmaker']"}),
            'fb_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'header': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'link': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'post_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'repost_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 2, 0, 0)'})
        }
    }

    complete_apps = ['neo_facebook']