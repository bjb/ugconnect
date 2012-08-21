# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Organization.comment'
        db.alter_column('publicpages_organization', 'comment', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Organization.howhear'
        db.alter_column('publicpages_organization', 'howhear', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Organization.graphicurl'
        db.alter_column('publicpages_organization', 'graphicurl', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Organization.linkurl'
        db.alter_column('publicpages_organization', 'linkurl', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

        # Changing field 'UserGroup.mailinglist'
        db.alter_column('publicpages_usergroup', 'mailinglist', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

    def backwards(self, orm):

        # Changing field 'Organization.comment'
        db.alter_column('publicpages_organization', 'comment', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Organization.howhear'
        db.alter_column('publicpages_organization', 'howhear', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Organization.graphicurl'
        db.alter_column('publicpages_organization', 'graphicurl', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Organization.linkurl'
        db.alter_column('publicpages_organization', 'linkurl', self.gf('django.db.models.fields.CharField')(default='', max_length=128))

        # Changing field 'UserGroup.mailinglist'
        db.alter_column('publicpages_usergroup', 'mailinglist', self.gf('django.db.models.fields.CharField')(default='', max_length=128))

    models = {
        'publicpages.organization': {
            'Meta': {'object_name': 'Organization'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contactinfo': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'contactname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'graphicurl': ('django.db.models.fields.TextField', [], {'default': "'images/unknown.png'", 'null': 'True', 'blank': 'True'}),
            'howhear': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkurl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'publicpages.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '16'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Organization']"})
        },
        'publicpages.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Organization']"})
        }
    }

    complete_apps = ['publicpages']