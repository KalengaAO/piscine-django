from django.shortcuts import render
from django.http import HttpResponse 
from . import models

# Create your views here.

def populate(request):
    movies_data = [
       {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19",
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16",
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19",
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kutz, Rick McCallum",
            "release_date": "1980-05-17",
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25",
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
        },
    ]

    result = []
    for movie in movies_data:
        try:
            obj, created = models.Movies.objects.get_or_create(**movie)

            if created:
                result.append(f"Ok {obj.title} inserted!")
            else:
                result.append(f"Ok {obj.title} already is exists!")

        except Exception as e:
            result.append(f"Error inserting {movie.get('title', 'error get title')}: {e}!")
    return HttpResponse("<br>".join(result))



def display(request):

    try:
        movies = models.Movies.objects.all()

        if not movies:
            return HttpResponse("No data available!")
        
        html = "<table border='1' style='border-collapse: collapse;'>"
        html += "<tr>" 
        html += "<th>Episode nb</th>"
        html += "<th>Title</th>" 
        html += "<th>Opening crawl</th>" 
        html += "<th>Director</th>" 
        html += "<th>Producer</th>" 
        html += "<th>Release Data</th></tr>"

        for movie in movies:
            html += "<tr>"
            html += f"<td>{movie.episode_nb}</td>"
            html += f"<td>{movie.title}</td>"
            opening_crawl = movies.opening_crawl if movie.opening_crawl else "N/A"
            html += f"<td>{opening_crawl}</td>"
            html += f"<td>{movie.director}</td>"
            html += f"<td>{movie.producer}</td>"
            html += f"<td>{movie.release_date}</td>"
            html += "</tr>"
        html += "</table>"

        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"No data available {e}")