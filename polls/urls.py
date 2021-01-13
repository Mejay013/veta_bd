from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.main, name='main'),
    path('person/', views.person, name='person')
]