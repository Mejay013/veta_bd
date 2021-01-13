from django.shortcuts import render
from django.http import HttpResponse
from .models import Countres,Artists,Persons,Genres,Countres,Groups
from django.core import serializers
from django.core.files import File


def index(request):
    countres = Countres.objects.all()
    context = {
        'countres' : countres
        }
    return render(request, "index.html", context=context)

def main(request,id):
    country = Countres.objects.filter(country_id = id).first()
    context = {
        'countres' : country
        }
    return render(request, "main.html", context=context)

def person(request):
    persons = Persons.objects.all()
    
    context = {
        'persons' : persons,
        }
    data = serializers.serialize("xml",persons)
    f = open('person.xml','w')
    report = File(f)
    report.write(data)

    report.close()
    return render(request, "artists.html", context=context)