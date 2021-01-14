from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Countres,Artists,Persons,Genres,Countres,Groups, Albums,AlbumSongs,Songs
from django.core import serializers
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib import auth 


def index(request):
    return redirect('person')

def main(request,id):
    country = Countres.objects.filter(country_id = id).first()
    context = {
        'countres' : country
        }
    return render(request, "main.html", context=context)


def main_tables(request):
    if not request.method == 'POST':
        countres = Countres.objects.all()
        genres = Genres.objects.all()
        groups = Groups.objects.all()

        context = {
            'countres':countres,
            'genres':genres,
            'groups':groups
        }

        return render(request,'main_tables.html', context=context)
        



def person(request):
    persons = Persons.objects.all()
    
    context = {
        'persons' : persons,
        }
    # data = serializers.serialize("xml",persons)
    # f = open('person.xml','w')
    # report = File(f)
    # report.write(data)

    # report.close()
    return render(request, "artists.html",context=context)


def new_person(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        sex = request.POST['sex']

        new_person = Persons( first_name = first_name, second_name = second_name, sex = sex)
        new_person.save()

        new_artist = Artists (artist_id = new_person.artist_id, genre_id = 1, country_id = 1,group_id = 1)
        new_artist.save()

        return redirect('person')
    else:
        return render(request,'new_person.html')

def album_songs(request,album_id):
    if request.method == 'POST':
        song_title = request.POST['song_name']

        new_song = Songs(song_title = song_title )
        new_song.save()

        album_songs = AlbumSongs(album_id = album_id, song_id = new_song.song_id)
        album_songs.save()

        return redirect('album_songs',album_id=album_id)
    else:
        songs_list = list()
        albums_songs = AlbumSongs.objects.filter(album_id = album_id)
        for songs in albums_songs:
            songs_list.append(Songs.objects.filter(song_id = songs.song_id))

        context = {
            'albums_songs':albums_songs,
            'songs_list':songs_list,
            'album_id':album_id
        }

        return render(request,'songs.html',context=context)

def change_person_info(request, person_id):
    if request.method == 'POST':
        person_id = request.POST['person_id']
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        sex = request.POST['sex']
        date = request.POST['date']
        genre = request.POST['genre']
        country = request.POST['country']
        group = request.POST['group']

        artist = Artists.objects.get(artist_id = person_id)
        artist.genre_id = genre
        artist.group_id = group
        artist.country_id = country
        artist.save()

        person = Persons.objects.get(artist_id = person_id)
        person.first_name = first_name
        person.second_name = second_name
        person.sex = sex
        person.birthday = date
        person.save()

        return redirect('person')

    else:
        album_songs = list()
        songs = list()
        person = Persons.objects.get(artist_id = person_id)
        artist = Artists.objects.get(artist_id = person.artist_id)
        genre = Genres.objects.all()
        country = Countres.objects.all()
        group = Groups.objects.all()

        albums = Albums.objects.filter(artist_id = person.artist_id)
        

        context = {
            'person' : person,
            'artist' :artist,
            'genre' :genre,
            'country' :country,
            'albums' :albums,
            'group': group,
            'artist_country': Countres.objects.get(country_id = artist.country_id).country_name,
            'artist_group': Groups.objects.get(group_id = artist.group_id).group_name,
            'artist_genre': Genres.objects.get(genre_id = artist.genre_id).genre_name
        }
        return render(request,'change_person.html',context=context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            error_msg = 'Неправильный логин или пароль'
            context = {
                'error_msg': error_msg
            }
            return render(request,'login.html',context=context)

    else:
        return render(request,'login.html')

def new_album(request, artist_id):
    album_title = request.POST['album_title']
    album_year = request.POST['album_year']

    new_album = Albums(artist_id = artist_id, album_title=album_title , album_year = album_year)
    new_album.save()

    return redirect('change_person_info', person_id = artist_id)

    
def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        password = request.POST['password']
        password1 = request.POST['password1']

        user = User.objects.create_user(username = username, password = password)
        user.save()

        user2 = auth.authenticate(username = username , password = password)
        auth.login(request, user2)

        
        return redirect('index')

    else:
        return render(request,'reg.html')

def rename_country(request):
    if request.method == 'POST':
        id = request.POST['country_id']
        new_name = request.POST['rename_country']

        update_country = Countres.objects.get(country_id = id)
        update_country.country_name = new_name
        update_country.save()

        return redirect('main_tables')

def rename_genre(request):
    if request.method == 'POST':
        id = request.POST['genre_id']
        new_name = request.POST['rename_genre']

        update_genre = Genres.objects.get(genre_id = id)
        update_genre.genre_name = new_name
        update_genre.save()

        return redirect('main_tables')
        
def rename_group(request):
    if request.method == 'POST':
        id = request.POST['group_id']
        new_name = request.POST['rename_group']

        update_group = Groups.objects.get(group_id = id)
        update_group.group_name = new_name
        update_group.save()

        return redirect('main_tables')
        


def add_country(request):
    if request.method == 'POST':
        country_name = request.POST['new_country']

        new_country = Countres(country_name = country_name)
        new_country.save()

        return redirect('main_tables')
    
def add_genre(request):
    if request.method == 'POST':
        genre_name = request.POST['new_genre']

        new_genre = Genres(genre_name = genre_name)
        new_genre.save()

        return redirect('main_tables')
    
def add_group(request):
    if request.method == 'POST':
        group_name = request.POST['new_group']

        new_group = Groups(group_name= group_name)
        new_group.save()

        return redirect('main_tables')
    
def logout(request):
    auth.logout(request)
    return redirect('index')