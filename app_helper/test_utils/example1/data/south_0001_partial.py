# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExampleModel1'
        db.create_table('example1_examplemodel1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('example1', ['ExampleModel1'])


    def backwards(self, orm):
        # Deleting model 'ExampleModel1'
        db.delete_table('example1_examplemodel1')


    models = {
        'example1.examplemodel1': {
            'Meta': {'object_name': 'ExampleModel1'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        }
    }

    complete_apps = ['example1']