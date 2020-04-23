from django.conf.urls import url
from django.urls import path
from . import views
from django.urls import path

#I'm not sure why but "path" makes it so that you can pass arguments and "url" doesn't

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^gethelp', views.GetHelp, name='gethelp'),
    url(r'^requestsUpdate', views.RequestsUpdate, name='requestsUpdate'),
    path('<int:form_id>/requestsUpdate/delete', views.DeleteSheet, name = 'delete'),
    path('confirm', views.confirm, name='confirm'),
    path('confirm_Accept', views.confirm_Accept, name='confirm'),
    path('confirm_Reject', views.confirm_Reject, name='confirm'),
    path('<str:tutor_username>/gethelp/', views.filloutform, name='fill'),
    url(r'^profile/update', views.Prof),
    url(r'^profile/viewprofile', views.SeeProfile),
    url(r'^account/logout/$', views.Logout),
    url(r'^send', views.Messaging, name='send'),
    path('<str:pal_username>/send/', views.CorLog, name='log'),
    path('<int:form_id>/givehelp/accept/', views.AcceptTutee, name='accepttutee'),
    path('<int:form_id>/givehelp/reject/', views.RejectTutee, name='rejecttutee'),
    url(r'^givehelp', views.GiveHelp),
    path('charge/', views.charge, name='charge'),
]
