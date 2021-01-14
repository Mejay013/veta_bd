from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.main, name='main'),
    path('reg', views.registration, name='reg'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('rename_country/', views.rename_country, name='rename_country'),
    path('rename_genre/', views.rename_genre, name='rename_genre'),
    path('rename_group/', views.rename_group, name='rename_group'),
    path('add_country', views.add_country, name='add_country'),
    path('add_genre', views.add_genre, name='add_genre'),
    path('add_group', views.add_group, name='add_group'),
    path('main_tables', views.main_tables, name='main_tables'),
    path('person/', views.person, name='person'),
    path('new_person/', views.new_person, name='new_person'),
    path('change_person/<int:person_id>', views.change_person_info, name='change_person'),
    path('new_album/<int:artist_id>', views.new_album, name='new_album'),
    path('album_songs/<int:album_id>', views.album_songs, name='album_songs')
]