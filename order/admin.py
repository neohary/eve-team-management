from django.contrib import admin
from .models import Order,regularOrderUnit
# Register your models here.

class regularOrderUnitInline(admin.TabularInline):
    model = regularOrderUnit
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    #list_display =  [field.name for field in Order._meta.get_fields()]
    list_display = ('uid','user','receiver','corp','itemcount','totalprice','status','createdate','finishdate')
    inlines = [regularOrderUnitInline]
    
@admin.register(regularOrderUnit)
class regularOrderUnitAdmin(admin.ModelAdmin):
    #list_display =  [field.name for field in regularOrderUnit._meta.get_fields()]
    list_display = ('uid','order','item','quantity','price','status')