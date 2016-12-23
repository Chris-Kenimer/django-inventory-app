from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'appointments'),
    url(r'^add_appointment$', views.add_appointment, name = 'add_appointment'),
    url(r'edit_appointment/(?P<id>\d+$)$', views.edit_appointment, name ='edit_appointment'),
    url(r'update_appointment$',views.update_appointment, name='update_appointment' ),
    url(r'remove_appointment/(?P<id>\d+$)$', views.remove_appointment, name="remove_appointment"),
]
