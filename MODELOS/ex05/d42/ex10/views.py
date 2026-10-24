from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .models import Movies, People, Planets
from django.views.decorators.csrf import csrf_exempt 
from .forms import SearchForm
import json 
import os
# Create your views here.

@csrf_exempt
def search_views(request):
    form = SearchForm(request.GET or None)
    movies = None

    if form.is_valid():
        min_date = form.cleaned_data["min_release_date"]
        max_date = form.cleaned_data["max_release_date"]
        diameter = form.cleaned_data["planet_diameter"]
        gender = form.cleaned_data["character_gender"]

        movies = (
            Movies.objects.filter(
                release_date__range=(min_date, max_date),
                characters__gender=gender,
                characters__homeworld__diameter__gte=diameter,
            ).distinct().prefetch_related("characters", "characters__homeworld")
        )

    return render(request, "ex10/search.html", {"form":form, "result": movies, "title": 'Filter'})

def populate(request):
    Movies.objects.all().delete()
    People.objects.all().delete()
    Planets.objects.all().delete()

    fixture_path = os.path.join(settings.BASE_DIR, "ex10_initial_data.json")

    try:
        with open(fixture_path, 'r') as file:
            data = json.load(file)

            for item in data:
                if item['model'] == "ex10.planets":
                    Planets.objects.create(pk=item['pk'], **item["fields"])

            for item in data:
                if item['model'] == "ex10.people"      :
                    fields = item['fields']
                    homeworld_pk = fields.pop("homeworld", None)

                    if homeworld_pk is not None:
                        homeworld_instance = Planets.objects.get(pk=homeworld_pk)
                        People.objects.create(pk=item["pk"], homeworld=homeworld_instance, **fields)
                    else:
                        People.objects.create(pk=item["pk"], homeworld=None, **fields)
            
            for item in data:
                if item['model'] == "ex10.movies":
                    if "characters" in item['fields']:
                        characters_pks = item['fields'].pop("characters")
                    else:
                        characters_pks = []
                    
                    movie = Movies.objects.create(pk=item['pk'], **item['fields'])
                
                    if characters_pks:
                        movie.characters.set(People.objects.filter(pk__in=characters_pks))
                
        return HttpResponse("Database populated succesfully.")
    except Exception as error:
        return HttpResponse(f"Error: {error}")