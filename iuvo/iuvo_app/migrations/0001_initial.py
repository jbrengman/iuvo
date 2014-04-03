# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table(u'iuvo_app_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('phone_str', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('phone_int', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'iuvo_app', ['Contact'])

        # Adding model 'Event'
        db.create_table(u'iuvo_app_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('start_day', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('start_time', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_day', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('end_time', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('notify_day', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('notify_time', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('notify_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'iuvo_app', ['Event'])

        # Adding M2M table for field contacts on 'Event'
        m2m_table_name = db.shorten_name(u'iuvo_app_event_contacts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'iuvo_app.event'], null=False)),
            ('contact', models.ForeignKey(orm[u'iuvo_app.contact'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'contact_id'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table(u'iuvo_app_contact')

        # Deleting model 'Event'
        db.delete_table(u'iuvo_app_event')

        # Removing M2M table for field contacts on 'Event'
        db.delete_table(db.shorten_name(u'iuvo_app_event_contacts'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'iuvo_app.contact': {
            'Meta': {'object_name': 'Contact'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'phone_int': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'phone_str': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'iuvo_app.event': {
            'Meta': {'object_name': 'Event'},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['iuvo_app.Contact']", 'symmetrical': 'False'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'end_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'end_time': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'notify_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'notify_time': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'start_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['iuvo_app']