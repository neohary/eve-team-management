from django.contrib import admin
from .models import Cart

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display =  [field.name for field in Cart._meta.get_fields()]