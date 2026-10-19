from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2

# Create your views here.

def get_connection():
    conf = {
        'dbname': settings.DATABASES['default']['NAME'],
        'user': settings.DATABASES['default']['USER'],
        'host': settings.DATABASES['default']['HOST'],
        'password': settings.DATABASES['default']['PASSWORD'],
        'port': 5432,
     }
    try:
        return psycopg2.connect(**conf)
    except psycopg2.PrommingError:
        return None

def init(request):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS ex04_movies(episode_nb 
                        INT PRIMARY KEY, title VARCHAR(64) NOT NULL, 
                        opening_crawl TEXT, director VARCHAR(32) NOT NULL, 
                        producer VARCHAR(128) NOT NULL, release_data DATE NOT NULL);
                    """
                )
        return HttpResponse('Ok')
    except Exception as error:
        return HttpResponse(f"Error to create a table: {error}")

def render_full_html_page(page_title: str, content: str) -> str:
    return f"""
            <!DOCTYPE html>
            <html lang="en>
                <head>
                    <meta charset= "UFT-8">
                    <title>{page_title}</title>
                </head>
                <body> 
                    <header>
                        <h1>{page_title}</h1>
                    </header>
                    <main>
                        <div>
                            {content}
                        </div>
                    </main>
                    </body> 
            </html>
        """

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

    try:
        conn = get_connection()
        if not conn:
            return HttpResponse("Error to connected in Database!")
        result = []
        for movie in movies_data:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ex04_movies(episode_nb, title, director, producer, release_data)
                    VALUES(%(episode_nb)s, %(title)s, %(director)s, %(producer)s, %(release_date)s)
                    ON CONFLICT (episode_nb) DO NOTHING;
                    """, movie,
            )
            if cursor.rowcount > 0:
                result.append(f"Ok: {movie['title']} inserted!")
                conn.commit()
            else:
                result.append(f"Error: {movie['title']} already inserted!")
                conn.rollback()
        return HttpResponse("<br>".join(result))
    except Exception as Error:
        return HttpResponse(f"<p style='color: red'>Error in populate data:</p> {Error}")
    finally:
        conn.close()

def display(request):
    conn = get_connection()
    if not conn:
        return HttpResponse("<p style='color: red'>Error to connected in database!</p>")
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM ex04_movies;
                """
            )
            movies = cursor.fetchall()
            headers = cursor.description
            content = None
            if not movies or not headers:
                return HttpResponse("error to get data")
            header = [head[0] for head in headers]
            content = "<table border='1' style='border-collapse: collapse; text-align: center;'><tr>"
            for head in header:
                content += f"<th>{head}</th>"
            content += "</tr>"
            for movie in movies:
                content += "<tr>"
                for mv in movie:
                    if not mv:
                        content += "<td>N/A</td>"
                    else:
                        content += f"<td>{mv}</td>"
                content += "</tr>"
            content += "</table>"
            full_page = render_full_html_page("Table of Movie", content)
            return HttpResponse(full_page)
    except Exception as Error:
        return HttpResponse(f"Error: {Error}")
    finally:
        conn.close()


@csrf_exempt 
def remove(request):
    try:
        content = None
        with get_connection() as conn:
            if request.method == "POST":
                title_to_remove = {}
                title_to_remove['title'] = request.POST.get('title')
                if title_to_remove:
                    with conn.cursor() as cursor:
                        cursor.execute(
                        """
                            DELETE FROM ex04_movies WHERE title = %(title)s;
                        """, title_to_remove,
                    )
                    conn.commit()

            with conn.cursor() as cursor:
                cursor.execute("SELECT title FROM ex04_movies;")
                movies = cursor.fetchall()

                if not movies:
                    content = "No data available!"
                else:
                    form_content = '<form method="post">'
                    form_content += '<select name="title">'
                    for movie in movies:
                        form_content += (
                            f'<option value="{movie[0]}">{movie[0]}</option>'
                        )
                    form_content += "</select>"
                    form_content += (
                            '<button type="submit" name="remove">Remove</button>'
                    )
                    form_content += "</form>"
                    content = form_content

        full_page = render_full_html_page("Remove a Movies", content)
        return HttpResponse(full_page)
    except Exception as e:
        full_page = render_full_html_page("", f"No data available!! {e}")
        return HttpResponse(full_page)