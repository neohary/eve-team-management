from django.urls import path
from cart import views
from django.conf.urls import url

urlpatterns = [
    path('',views.myCartListView,name='my-cart'),
    path('delete_cart/<int:pk>',views.delete_cart,name='delete-cart'),
    path('add_cart/<int:item>',views.add_cart,name='add-cart'),
    path('update_cart/<int:pk>',views.update_cart,name='update-cart'),
]