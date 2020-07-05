from django.urls import path
from corp import views
from django.conf.urls import url

urlpatterns = [
    path('',views.index,name='index'),
    #path('character/<int:pk>',views.characterInfView.as_view(),name='character-detail'),
    path('<int:pk>',views.corpInfView.as_view(),name='corp-detail'),
    path('<int:pk>/storage',views.invStorageView.as_view(),name='InvStorage-list'),
    path('<int:pk>/storage/paste-storage-update/',views.paste_storage_update,name='paste-storage-update'),
]
urlpatterns += [
    path('character/create/',views.CharacterCreate.as_view(),name='character_create'),
    #path('character/<int:pk>/update',views.CharacterUpdate.as_view(),name='character_update'),
    path('character/<int:pk>/delete',views.CharacterDelete.as_view(),name='character_delete'),
    path('charactermanage/',views.UserCharactersListView.as_view(),name='character-manage'),
    path('profile/',views.update_profile,name='profile'),
    path('profile/changename',views.update_username,name='changeusername'),
]

urlpatterns += [
    path('<int:pk>/hr/verification/',views.verification_list,name='verification-list'),
    path('hr/verification/accept/<int:pk>',views.verification_accept,name='verification-accept'),
    path('hr/verification/reject/<int:pk>',views.verification_reject,name='verification-reject'),
    path('verification/<int:pk>/submit/',views.submit_verification,name='submit-verification'),
]

urlpatterns += [
    path('<int:pk>/edit',views.corpInfUpdate,name='corp-update'),
    path('<int:pk>/miniblog/post',views.corpMiniBlog_post,name='corp-blog-post'),
    path('<int:cpk>/miniblog/<int:pk>/delete',views.corpMiniBlog_delete,name='corp-blog-delete'),
    path('<int:pk>/memlist',views.corpMemberListView.as_view(),name='corp-mem-list'),
]

urlpatterns += [
    path('create/',views.EveCorporationCreateView.as_view(),name='corp-create'),

]

















