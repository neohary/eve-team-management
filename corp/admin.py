from django.contrib import admin
from .models import EveCorporation,EveCharacter,InvStorage,EveAlliance,Profile,corpMiniBlog
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from sde.models import Invtypes
#from sde.admin import InvtypesInline
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
        
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
    list_display = ('name','corp','bounduser','ingame_id')
#admin.site.register(InvStorage)
#@admin.register(InvStorage)
#class InvStorageAdmin(admin.ModelAdmin):
#    list_display = ('typeid','stock')

class InvStorageInline(admin.TabularInline):
    model = InvStorage
    
@admin.register(InvStorage)
class InvStorageAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in InvStorage._meta.get_fields()]
    #inlines = [InvtypesInline]
    
@admin.register(corpMiniBlog)
class corpMiniBlogAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in corpMiniBlog._meta.get_fields()]