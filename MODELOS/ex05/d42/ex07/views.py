from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from . import models, forms

# Create your views here.

def render_html_page(title: str, content: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='UTF-8'>
                <title>{title}</title>
            </head>
            </body>
                <h1>{title}</h1>
                <main>
                    {content}
                </main>
            </body>
        </html>
        """

def populate(request):
    movies_data = [
          {
            "episode_nb": 1, "title": "The Phantom Menace",
            "director": "George Lucas", "producer": "Rick McCallum",
            "release_date": "1999-05-19",
        },
        {
            "episode_nb": 2, "title": "Attack of the Clones",
            "director": "George Lucas", "producer": "Rick McCallum",
            "release_date": "2002-05-16",
        },
        {
            "episode_nb": 3, "title": "Revenge of the Sith",
            "director": "George Lucas", "producer": "Rick McCallum",
            "release_date": "2005-05-19",
        },
        {
            "episode_nb": 4, "title": "A New Hope",
            "director": "George Lucas", "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
        },
        {
            "episode_nb": 5, "title": "The Empire Strikes Back",
            "director": "Irvin Kershner", "producer": "Gary Kutz, Rick McCallum",
            "release_date": "1980-05-17",
        },
        {
            "episode_nb": 6, "title": "Return of the Jedi",
            "director": "Richard Marquand", "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25",
        },
        {
            "episode_nb": 7, "title": "The Force Awakens",
            "director": "J. J. Abrams", "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
        },
    ]
    result = []
    try:
        for movie in movies_data:
            obj, created = models.Movies.objects.get_or_create(**movie)
            if created:
                result.append(f"{movie['title']} inserted!")
            else:
                result.append(f"{movie['title']} is already inserted!")
        html_page = render_html_page("Populate database!", "<br>".join(result))
        return HttpResponse(html_page)
    except Exception as error:
        return HttpResponse(f"<p style='color: ref;'>Error</p>{error}")


def display(request):
    try:
        movies = models.Movies.objects.all().values()
        if not movies:
            return HttpResponse("No data available!")
        content = "<table border='1' style='border-collapse: collapse; text-align: center'><tr>"
        content += "<th>Episode_nb</th>"
        content += "<th>Title</th>"
        content += "<th>Opening_crawl</th>"
        content += "<th>director</th>"
        content += "<th>Producer</th>"
        content += "<th>Release date</th></tr>"
        for mov in movies:
            content += f"<tr><td>{mov['episode_nb']}</td>"
            content += f"<td>{mov['title']}</td>"
            content += f"<td>{mov['opening_crawl'] if mov['opening_crawl'] else 'N/A'}</td>"
            content += f"<td>{mov['director']}</td>"
            content += f"<td>{mov['producer']}</td>"
            content += f"<td>{mov['release_date']}</td></tr>"
        content += "</table>"
        return HttpResponse(render_html_page("List of movies", content))
    except Exception as error:
        return HttpResponse(f"Error: {error}")

@csrf_exempt
def remove(request):
    try:

        if request.method == 'POST':
            episode_nb = request.POST.get('episode_nb')
            if episode_nb:
                movies_to_delete = models.Movies.objects.get(pk=episode_nb)
                movies_to_delete.delete()
        movies = models.Movies.objects.all().values()
        if movies:
            return HttpResponse(f"No data available!")
        form_content = "<form method='post'>"
        form_content += "<select name='episode_nb'>"
        for mov in movies:
            form_content += f"<option value='{mov['episode_nb']}'>{mov['episode_nb']}</option>"
        form_content += "</select>"
        form_content += "<button type='submit'>Delete</button></form>"
        return HttpResponse(render_html_page("List of movies to remove", form_content))
    except Exception as error:
        return HttpResponse(f"Error: {error}")


@csrf_exempt
def update(request):
    if not models.Movies.objects.all():
        return HttpResponse("No data available!")
    try:
        if request.method == 'POST':
            form = forms.updateForm(request.POST)
            if form.is_valid():
                movie_to_update = form.cleaned_data['movie']
                new_crawl = form.cleaned_data['opening_crawl']

                movie_to_update.opening_crawl = new_crawl
                movie_to_update.save()

                return redirect("update")
        form = forms.updateForm()
        return render(request, "ex07/index.html", {'form': form})
    except Exception as error:
        return HttpResponse(f"Error: {error}")
