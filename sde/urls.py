from django.urls import path
from sde import views
from django.conf.urls import url

urlpatterns = [
    url(r'^marketgroups',views.show_marketgroups,name='marketgroups'),
    path('marketgroup/<int:pk>',views.itemListView.as_view(),name='invtypes_list'),
    path("marketgroup/",views.itemListSearchView,name='invtypes_list'),
]

urlpatterns += [
    path('invtypelist',views.invtypeListView.as_view(),name='item_list'),
    path('dropsde',views.delete_all_sde_data,name='dropsde'),
]