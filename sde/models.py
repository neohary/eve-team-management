# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from mptt.models import MPTTModel,TreeForeignKey
from django.urls import reverse


class Eveicons(models.Model):
    iconid = models.AutoField(db_column='iconID',primary_key=True)  # Field name made lowercase.
    iconfile = models.TextField(db_column='iconFile', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    obsolete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'eveIcons'
        
    def __str__(self):
        return self.iconfile.replace('res:','')


class Invtypes(models.Model):
    typeid = models.AutoField(db_column='typeID',primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupID', blank=True, null=True)  # Field name made lowercase.
    typename = models.TextField(db_column='typeName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    description = models.TextField(blank=True, null=True)
    mass = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume = models.TextField(blank=True, null=True)  # This field type is a guess.
    packagedvolume = models.TextField(db_column='packagedVolume', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    capacity = models.TextField(blank=True, null=True)  # This field type is a guess.
    portionsize = models.IntegerField(db_column='portionSize', blank=True, null=True)  # Field name made lowercase.
    factionid = models.IntegerField(db_column='factionID', blank=True, null=True)  # Field name made lowercase.
    raceid = models.TextField(db_column='raceID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    baseprice = models.TextField(db_column='basePrice', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    published = models.IntegerField(blank=True, null=True)
    marketgroupid = models.ForeignKey('Marketgroups',on_delete=models.SET_NULL, db_column='marketgroupID', blank=True, null=True)  # Field name made lowercase.
    graphicid = models.IntegerField(db_column='graphicID', blank=True, null=True)  # Field name made lowercase.
    radius = models.TextField(blank=True, null=True)  # This field type is a guess.
    iconid = models.IntegerField(db_column='iconID', blank=True, null=True)  # Field name made lowercase.
    soundid = models.IntegerField(db_column='soundID', blank=True, null=True)  # Field name made lowercase.
    soffactionname = models.TextField(db_column='sofFactionName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sofmaterialsetid = models.IntegerField(db_column='sofMaterialSetID', blank=True, null=True)  # Field name made lowercase.
    metagroupid = models.IntegerField(db_column='metaGroupID', blank=True, null=True)  # Field name made lowercase.
    variationparenttypeid = models.IntegerField(db_column='variationparentTypeID', blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('invtype-detail', args=[str(self.typeid)])
    
    def __str__(self):
        return '%s (%s)' % (self.typename,self.typeid)
        
    class Meta:
        managed = True
        db_table = 'invTypes'
        


class Marketgroups(MPTTModel):
    marketgroupid = models.AutoField(db_column='marketGroupID',primary_key=True)  # Field name made lowercase.
    descriptionid = models.TextField(db_column='descriptionID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hastypes = models.IntegerField(db_column='hasTypes', blank=True, null=True)  # Field name made lowercase.
    iconid = models.IntegerField(db_column='iconID', blank=True, null=True)  # Field name made lowercase.
    nameid = models.TextField(db_column='nameID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    parentgroupid = TreeForeignKey('self', on_delete=models.CASCADE, db_column='parentGroupID', blank=True, null=True, related_name='children')  # Field name made lowercase.

    
    def get_absolute_url(self):
        return reverse('invtypes_list', args=[str(self.marketgroupid)])
        
    def __str__(self):
        return '%s (%s)' % (self.nameid, self.marketgroupid)
            
    class Meta:
        managed = True
        db_table = 'marketGroups'
        permissions = (("user_can_use_market","用户访问市场数据的权限"),)
    
    class MPTTMeta:
        order_insertion_by = ['marketgroupid']
        parent_attr = 'parentgroupid'
        
