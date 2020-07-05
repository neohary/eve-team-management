from django.urls import path
from django.conf.urls import url
from core import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('notice/list/',views.NoticeListView.as_view(),name='notice-list'),
    path('notice/update/',views.UpdateNotice,name='notice-update'),
    path('donate/',views.donateInfoListView.as_view(),name='donate-list'),
	path('donate/add',views.addDonater,name='donate-add'),
    path('about/',views.about,name="about"),
]