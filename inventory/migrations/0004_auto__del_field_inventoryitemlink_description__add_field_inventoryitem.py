# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'InventoryItemLink.description'
        db.delete_column('inventory_inventoryitemlink', 'description')

        # Adding field 'InventoryItemLink.relationship'
        db.add_column('inventory_inventoryitemlink', 'relationship',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'InventoryItemLink.description'
        db.add_column('inventory_inventoryitemlink', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Deleting field 'InventoryItemLink.relationship'
        db.delete_column('inventory_inventoryitemlink', 'relationship')


    models = {
        'inventory.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            'container_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'max_per_container': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'orderable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.InventoryItem']", 'through': "orm['inventory.InventoryItemLink']", 'symmetrical': 'False'})
        },
        'inventory.inventoryitemlink': {
            'Meta': {'object_name': 'InventoryItemLink'},
            'child_inventory_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['inventory.InventoryItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_child_inventory_items_required': ('django.db.models.fields.IntegerField', [], {}),
            'parent_inventory_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['inventory.InventoryItem']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']