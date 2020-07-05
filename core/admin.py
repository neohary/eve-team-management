from django.contrib import admin
from .models import generalInfo,donateInfo
# Register your models here.

@admin.register(generalInfo)
class generalInfoAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in generalInfo._meta.get_fields()]
    
@admin.register(donateInfo)
class donateInfoAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in donateInfo._meta.get_fields()]