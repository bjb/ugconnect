# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

        for ug2 in orm.UserGroup2.objects.all ():
            ugs = orm.UserGroup.objects.filter (organization__name__exact = ug2.name)

            if 0 < ugs.count ():
                if 1 < ugs.count ():
                    raise StandardError ('Not expecting more than one group for %s' % ug2.name)
                ug = ugs[0]
                ug.meet_weekday = ug2.meet_weekday
                ug.meet_week_of_month = ug2.meet_week_of_month
                ug.meet_description = ug2.meet_description
                ug.location_name = ug2.location_name
                ug.location_address = ug2.location_address
                ug.location_note = ug2.location_note
                ug.meeting_time = ug2.meeting_time
                ug.web_site = ug2.web_site
                ug.email_site = ug2.email_site
                ug.other_url = ug2.other_url
                ug.confirmed = True

            else:

                # get/create an Organization
                orgs = orm.Organization.objects.filter (name__exact = ug2.name)
                if 0 < orgs.count ():
                    if 1 < orgs.count ():
                        raise StandardError ('Not expecting more than 1 Organization for %s' % ug2.name)
                    org = orgs[0]
                    if org.linkurl != ug2.web_site:
                        raise StandardError ('linkurl and web_site are not the same for %s:  %s vs %s' % (ug2.name, ug2.web_site, org.linkurl))
                else:
                    org = orm.Organization ()
                    org.name = ug2.name
                    org.contactname = ('unknown')
                    org.contactinfo = ('unknown@example.com')
                    org.date_created = datetime.date.today ()
                    org.linkurl = ug2.web_site
                    org.save ()

                # create a UserGroup
                ug = orm.UserGroup ()
                ug.organization = org

                ug.date_created = datetime.date.today ()
            ug.save ()



    def backwards(self, orm):
        pass

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'publicpages.bzflagteam': {
            'Meta': {'object_name': 'BzflagTeam'},
            'captain': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'contactinfo': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "'images/default_bzflag_icon.png'", 'max_length': '100'}),
            'icon_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'navigator': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'padre': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teamname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'weapons_specialist': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'publicpages.organization': {
            'Meta': {'object_name': 'Organization'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contactinfo': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'contactname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'howhear': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'linkurl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "'unknown.png'", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'publicpages.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Sponsor']"})
        },
        'publicpages.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '16'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Organization']"})
        },
        'publicpages.theme': {
            'Meta': {'object_name': 'Theme'},
            'bullet': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'favicon': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'headergraphic': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'publicpages.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'email_site': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'location_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mailinglist': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'meet_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meet_week_of_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meet_weekday': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Organization']"}),
            'other_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'web_site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'publicpages.usergroup2': {
            'Meta': {'object_name': 'UserGroup2'},
            'email_site': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'location_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meet_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meet_week_of_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meet_weekday': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'other_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'usergroup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.UserGroup']", 'null': 'True', 'blank': 'True'}),
            'web_site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'publicpages.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publicpages.Theme']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['publicpages']
    symmetrical = True
