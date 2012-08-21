# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table('publicpages_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('contactname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('contactinfo', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('linkurl', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('howhear', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('publicpages', ['Organization'])

        # Adding model 'Sponsor'
        db.create_table('publicpages_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publicpages.Organization'])),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('publicpages', ['Sponsor'])

        # Adding model 'UserGroup'
        db.create_table('publicpages_usergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publicpages.Organization'])),
            ('mailinglist', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('publicpages', ['UserGroup'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table('publicpages_organization')

        # Deleting model 'Sponsor'
        db.delete_table('publicpages_sponsor')

        # Deleting model 'UserGroup'
        db.delete_table('publicpages_usergroup')


    models = {
        'publicpages.organization': {
            'Meta': {'object_name': 'Organization'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'contactinfo': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'contactname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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