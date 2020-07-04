from django.urls import path
from order import views
from django.conf.urls import url

urlpatterns = [
    path('',views.orderListView.as_view(),name='my-orders'),
    path('create/',views.create_order,name='create-order'),
    path('<str:pk>',views.orderDetailView.as_view(),name='order-detail'),
    path('cancel/<str:pk>',views.cancel_order,name='cancel-order'),
]

urlpatterns += [
    path('manage/corp',views.orderListViewCorp.as_view(),name='order-list-corp'),
    path('manage/<str:pk>',views.orderManageDetail.as_view(),name='order-manage-detail'),
    path('update/<str:pk>',views.update_orderunit,name='update-orderunit'),
    path('complete/<str:pk>',views.complete_order,name='complete-order'),
]