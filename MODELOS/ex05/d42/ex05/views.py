from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
    for movies in movies_data:
        try:
            obj, created = models.Movies.objects.get_or_create(**movies)
        
            if created:
                result.append(f"movie {obj.title} inserted!")
            else:
                result.append(f"movie: {obj.title} already inserted!")
        except Exception as error:
            return HttpResponse(f"Error: {error}!")
    return HttpResponse("<br>".join(result))


def display(request):
    content = ""
    try:
        obj = models.Movies.objects.all().values()
        if not obj:
            content = "No avaliable data!"
        else:
            content += "<table border='1' style='border-collapse: collapse;'><tr><th>Episode_nb</th><th>Title</th><th>Text</th><th>Director</th><th>Producer</th><th>release Date</th></tr>"
            for o in obj:
                content += f"<tr><td>{o['episode_nb']}</td>"
                content += f"<td>{o['title']}</td>"
                content += f"<td>{o['opening_crawl'] if o['opening_crawl'] else 'N/A'}</td>"
                content += f"<td>{o['director']}</td>"
                content += f"<td>{o['producer']}</td>"
                content += f"<td>{o['release_date']}</td>"
                
            content += "</tr></table>"
        return HttpResponse(content)
    except Exception as error:
        return HttpResponse(f"Error: {error}")


@csrf_exempt
def remove(request):
    try:
        if request.method == "POST":
            episode_nb = request.POST.get('episode_nb')
            if episode_nb:
                try:
                    movie_to_delete = models.Movies.objects.get(pk=episode_nb)
                    movie_to_delete.delete()
                except models.Movies.DoesNotExist:
                    return None 

        movies = models.Movies.objects.all()

        form_content = "<form method='post'>"
        form_content += "<select name='episode_nb'>"
        for movie in movies:
            form_content += f"<option value='{movie.episode_nb}'>{movie.episode_nb}</option>"
        form_content += "</select>"
        form_content += "<button type='submit'>Delete</button></form>"
        return HttpResponse(form_content)
    except Exception as error:
        return HttpResponse(f"Error {error}")