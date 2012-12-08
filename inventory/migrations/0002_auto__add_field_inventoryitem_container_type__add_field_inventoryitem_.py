# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InventoryItem.container_type'
        db.add_column('inventory_inventoryitem', 'container_type',
                      self.gf('django.db.models.fields.TextField')(default='Box'),
                      keep_default=False)

        # Adding field 'InventoryItem.max_per_container'
        db.add_column('inventory_inventoryitem', 'max_per_container',
                      self.gf('django.db.models.fields.IntegerField')(default=100),
                      keep_default=False)


        # Changing field 'InventoryItem.name'
        db.alter_column('inventory_inventoryitem', 'name', self.gf('django.db.models.fields.TextField')())
        # Adding field 'InventoryItemLink.description'
        db.add_column('inventory_inventoryitemlink', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'InventoryItem.container_type'
        db.delete_column('inventory_inventoryitem', 'container_type')

        # Deleting field 'InventoryItem.max_per_container'
        db.delete_column('inventory_inventoryitem', 'max_per_container')


        # Changing field 'InventoryItem.name'
        db.alter_column('inventory_inventoryitem', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Deleting field 'InventoryItemLink.description'
        db.delete_column('inventory_inventoryitemlink', 'description')


    models = {
        'inventory.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            'container_type': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'max_per_container': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'orderable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.InventoryItem']", 'through': "orm['inventory.InventoryItemLink']", 'symmetrical': 'False'})
        },
        'inventory.inventoryitemlink': {
            'Meta': {'object_name': 'InventoryItemLink'},
            'child_inventory_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['inventory.InventoryItem']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_child_inventory_items_required': ('django.db.models.fields.IntegerField', [], {}),
            'parent_inventory_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['inventory.InventoryItem']"})
        }
    }

    complete_apps = ['inventory']