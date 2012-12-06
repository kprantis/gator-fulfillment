# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InventoryItem'
        db.create_table('inventory_inventoryitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('orderable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('inventory', ['InventoryItem'])

        # Adding model 'InventoryItemLink'
        db.create_table('inventory_inventoryitemlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_inventory_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['inventory.InventoryItem'])),
            ('child_inventory_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['inventory.InventoryItem'])),
            ('num_child_inventory_items_required', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('inventory', ['InventoryItemLink'])


    def backwards(self, orm):
        # Deleting model 'InventoryItem'
        db.delete_table('inventory_inventoryitem')

        # Deleting model 'InventoryItemLink'
        db.delete_table('inventory_inventoryitemlink')


    models = {
        'inventory.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'orderable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.InventoryItem']", 'through': "orm['inventory.InventoryItemLink']", 'symmetrical': 'False'})
        },
        'inventory.inventoryitemlink': {
            'Meta': {'object_name': 'InventoryItemLink'},
            'child_inventory_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['inventory.InventoryItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_child_inventory_items_required': ('django.db.models.fields.IntegerField', [], {}),
            'parent_inventory_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['inventory.InventoryItem']"})
        }
    }

    complete_apps = ['inventory']