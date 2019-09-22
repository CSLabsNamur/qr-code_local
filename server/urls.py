from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('synchro', views.synchronization_view, name='synchronization'),
    path('location/<str:name>', views.location_view, name='location')
]
