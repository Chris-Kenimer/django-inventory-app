from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'quotes'),
    url(r'^add_quote$', views.add_quote, name='add_quote'),
    url(r'^favorite_a_quote$', views.favorite_a_quote, name='favorite_a_quote'),
    url(r'^remove_favorite$', views.remove_favorite, name='remove_favorite'),
]
