from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import psycopg2

# Create your views here.
def get_conection():
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES.get('default', {}).get('NAME', 'dbtest'),
            user=settings.DATABASES.get('default', {}).get('USER', 'usertest'),
            password=settings.DATABASES.get('default', {}).get('PASSWORD', '123test'),
            port=5432,
            host=settings.DATABASES.get('default', {}).get('HOST', 'Localhost'),
        )
        return conn
    except psycopg2.OperationalError as error:
        print(f"An err")
        return None

def render_full_html_page(page_title: str, content: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{page_title}</title>
            </head>
            <body>
                <header>
                    <h1>{page_title}</h1>
                </header>
                <hr>
                <main>
                    <div>
                        {content}
                    </div>
                </main>
            </body>
        </html>
        """

def init(request):
    conn = None
    conn = get_conection()
    if not conn:
        return httpResponse("Errror: could not connect to the database.")
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ex02_movies(
                    episode_nb INT PRIMARY KEY,
                    title VARCHAR(64) UNIQUE NOT NULL,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(64) NOT NULL,
                    release_date DATE NOT NULL
                );
                """
            )
            conn.commit()
            return HttpResponse("Ok")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    finally:
        conn.close()

def populate(request):
    movies_data = [
        {
            'episode_nb': 1 ,
            'title': 'The Phantom Menace',
            'director': 'George Lucas',
            'producer' : 'Rick McCallum',
            'release_date': '1999-05-19',},
            {
            'episode_nb': 2 ,
            'title': 'Attack of the Clones',
            'director': 'George Lucas',
            'producer' : 'Rick McCallum',
            'release_date': '2002-05-16',},
            {
            'episode_nb': 3 ,
            'title': 'Revenge of the Sith',
            'director': 'George Lucas',
            'producer' : 'Rick McCallum',
            'release_date': '2005-05-19',},
            {
            'episode_nb': 4,
            'title': 'A New Hope',
            'director': 'George Lucas',
            'producer' : 'Gary Kurtz, Rick McCallum',
            'release_date': '1977-05-25',},
            {
            'episode_nb': 5 ,
            'title': 'The Empire Strikes Back',
            'director': 'Irvin Kershner',
            'producer' : 'Gary Kurtz, Rick McCallum',
            'release_date': '1980-05-17',},
            {
            'episode_nb': 6,
            'title': 'Return of the Jedi',
            'director': 'Richard Marquand',
            'producer' : 'Howard G. Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25',},
            {
            'episode_nb': 7 ,
            'title': 'The Force Awakens',
            'director': 'J. J. Abrams',
            'producer' : 'Kathleen Kennedy, J. J. Abrams, Bryan Burk',
            'release_date': '2015-12-11',},
    ]

    conn = get_conection()
    if not conn:
        return HttpResponse("Error: could not connect to the database.")
    
    results = []
    try:
        with conn.cursor() as cursor:
            for movies in movies_data:
                try:
                    cursor.execute(
                        """
                            INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
                            VALUES (%(episode_nb)s, %(title)s, %(director)s, %(producer)s, %(release_date)s)
                            ON CONFLICT (episode_nb) DO NOTHING;
                        """, movies,
                    )
                    if cursor.rowcount > 0:
                        results.append(f"Ok: {movies.get('title', 'error title')} inserted.")
                        conn.commit()
                    else:
                        results.append(f"Ok: {movies.get('title', 'error title')} already exists")
                except Exception as e:
                    results.append(f"Error insertion {movies.get('title', 'error title')}: {e}")
                    conn.rollback()
            return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"<p style='color:red'>An unexpected error ocurred: {e}</p>")
    finally:
        conn.close()


def display(request):
    try:
        with get_conection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM ex02_movies;")
                movies = cursor.fetchall()
                if not movies:
                    content = "no data available"
                else:
                    table_content = "<table border='1' style='border-collapse: collapse; text-align: center;'><tr>"
                    headers = [desc[0] for desc in cursor.description]
                    print(headers)
                    for header in headers:
                        table_content += f"<th>{header}</th>"
                    table_content += "</tr>"

                    for movie in movies:
                        table_content += "<tr>"
                        for coll in movie:
                            table_content += (f"<td>{coll if coll is not None else 'N/A'}</td>")
                        table_content += "</tr>"
                    table_content += "</table>"
                    content = table_content

        full_page = render_full_html_page("Movies list (ex02)", content)
        return HttpResponse(full_page)
    except Exception as e:
        full_page = render_full_html_page("Error page", "<p style='color:red;'>No data available</p>")
        return HttpResponse(full_page)