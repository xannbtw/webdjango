from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_view, name='inicio'), 
    path('nosotros/', views.catalogo_view, name='nosotros'),
]