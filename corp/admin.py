from django.contrib import admin
from .models import EveCorporation,EveCharacter,InvStorage,EveAlliance
from sde.models import Invtypes
#from sde.admin import InvtypesInline
# Register your models here.

class EveCorporationInline(admin.TabularInline):
	model = EveCorporation

@admin.register(EveAlliance)
class EveAllianceAdmin(admin.ModelAdmin):
	list_display = ('name','codename','ingame_id')
	inlines = [EveCorporationInline]

#admin.site.register(EveCorporation)
@admin.register(EveCorporation)
class EveCorporationAdmin(admin.ModelAdmin):
	list_display = ('name','alliance','ceo','codename','ingame_id','dftdiscount')
#admin.site.register(EveCharacter)
@admin.register(EveCharacter)
class EveCharacterAdmin(admin.ModelAdmin):
	list_display = ('name','corp')
#admin.site.register(InvStorage)
#@admin.register(InvStorage)
#class InvStorageAdmin(admin.ModelAdmin):
#	list_display = ('typeid','stock')

class InvStorageInline(admin.TabularInline):
	model = InvStorage
	
@admin.register(InvStorage)
class InvStorageAdmin(admin.ModelAdmin):
	list_display =  [field.name for field in InvStorage._meta.get_fields()]
	#inlines = [InvtypesInline]