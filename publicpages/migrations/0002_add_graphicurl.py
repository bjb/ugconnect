# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Organization.graphicurl'
        db.add_column('publicpages_organization', 'graphicurl',
                      self.gf('django.db.models.fields.TextField')(default='images/unknown.png'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Organization.graphicurl'
        db.delete_column('publicpages_organization', 'graphicurl')


    models = {
        'publicpages.organization': {
            'Meta': {'object_name': 'Organization'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'contactinfo': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'contactname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'graphicurl': ('django.db.models.fields.TextField', [], {'default': "'images/unknown.png'"}),
            'howhear': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkurl': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'publicpages.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Organization']"})
        },
        'publicpages.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Organization']"})
        }
    }

    complete_apps = ['publicpages']