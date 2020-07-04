from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Eveicons,Invtypes,Marketgroups
from corp.admin import InvStorageInline

class InvtypesInline(admin.TabularInline):
    model = Invtypes
    extra = 0

admin.site.register(Marketgroups,MPTTModelAdmin)

@admin.register(Invtypes)
class InvtypesAdmin(admin.ModelAdmin):
    #list_display =  [field.name for field in Invtypes._meta.get_fields()]
    list_display = ('typeid','typename')
    inlines = [InvStorageInline]

@admin.register(Eveicons)
class EveiconsAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in Eveicons._meta.get_fields()]