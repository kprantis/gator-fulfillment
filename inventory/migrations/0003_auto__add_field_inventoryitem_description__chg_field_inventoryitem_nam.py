# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InventoryItem.description'
        db.add_column('inventory_inventoryitem', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


        # Changing field 'InventoryItem.name'
        db.alter_column('inventory_inventoryitem', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'InventoryItem.container_type'
        db.alter_column('inventory_inventoryitem', 'container_type', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'InventoryItemLink.description'
        db.alter_column('inventory_inventoryitemlink', 'description', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):
        # Deleting field 'InventoryItem.description'
        db.delete_column('inventory_inventoryitem', 'description')


        # Changing field 'InventoryItem.name'
        db.alter_column('inventory_inventoryitem', 'name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'InventoryItem.container_type'
        db.alter_column('inventory_inventoryitem', 'container_type', self.gf('django.db.models.fields.TextField')())

        # Changing field 'InventoryItemLink.description'
        db.alter_column('inventory_inventoryitemlink', 'description', self.gf('django.db.models.fields.TextField')())

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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_child_inventory_items_required': ('django.db.models.fields.IntegerField', [], {}),
            'parent_inventory_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['inventory.InventoryItem']"})
        }
    }

    complete_apps = ['inventory']