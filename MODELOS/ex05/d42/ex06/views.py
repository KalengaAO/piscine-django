from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2

# Create your views here.

def get_connection():
    config = {
        'dbname': settings.DATABASES['default']['NAME'],
        'user': settings.DATABASES['default']['USER'],
        'password': settings.DATABASES['default']['PASSWORD'],
        'host': settings.DATABASES['default']['HOST'],
        'port': 5432,
    }

    try:
        return psycopg2.connect(**config)
    except psycopg2.ProgrammingError:
        return None
        

def init(request):
    sql_table = """
            CREATE TABLE IF NOT EXISTS ex06_movies(
            episode_nb INT PRIMARY KEY,
            title VARCHAR(64) NOT NULL, 
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL, 
            producer VARCHAR(128) NOT NULL, 
            release_date DATE NOT NULL,
            created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), 
            updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
            );            
        """

    sql_create_function = """
            CREATE OR REPLACE FUNCTION update_changetimestamtp_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated = NOW();
                NEW.created = OLD.created;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """

    sql_create_trigger = """
            DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;
            CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE ON
            ex06_movies FOR EACH ROW EXECUTE PROCEDURE 
            update_changetimestamtp_column();
        """
   
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_table)
                cursor.execute(sql_create_function)
                cursor.execute(sql_create_trigger)
        return HttpResponse("OK")
    except Exception as error:
        return HttpResponse(f"<p style='color: red'>Error:<p>{error}")

def populate(request):
    movie_data = [
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
    sql_insert = """
            INSERT INTO ex06_movies(episode_nb, title, director, producer, release_date)
            VALUES (%(episode_nb)s, %(title)s, %(director)s, %(producer)s, %(release_date)s)
            ON CONFLICT (episode_nb) DO NOTHING;
        """
    result = []
    conn = get_connection()
    if not conn:
        return HttpResponse("Error to connected with database!")
    try:
        with conn.cursor() as cursor:
            for movie in movie_data:
                cursor.execute(sql_insert, movie)
                if cursor.rowcount > 0:
                    result.append(f"{movie['title']} is inserted!")
                    conn.commit()
                else:
                    result.append(f"{movie['title']} is already inserted!")
                    conn.rollback()
        return HttpResponse("<br>".join(result))
    except Exception as error:
        return HttpResponse(f"<p style='color: red'>Error:</p>{error}")
    finally:
        conn.close()

def display(request):
    sql_select = """
            SELECT * FROM ex06_movies;
        """
    conn = get_connection()
    content = None
    if not conn:
        return HttpResponse("Error to connected in database!")
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_select)
            movies = cursor.fetchall()
            headers = cursor.description 
            cursor.close()
            if not movies:
                return HttpResponse("No data avaliable!")
            header = [head[0] for head in headers]
            content = "<table border='1' style='border-collapse: collapse; text-align: center;'><tr>"
            for heads in header:
                content += f"<th>{heads}</th>"
            content += "</tr>"
            for movie in movies:
                content += "<tr>"
                for mov in movie:
                    if mov:
                        content += f"<td>{mov}</td>"
                    else:
                        content += f"<td>N/A</td>"
                content += "</tr>"
            content += "</table>"
        return HttpResponse(content)
    except Exception as error:
        return HttpResponse(f"Error: {error}")
    finally:
        conn.close()

def render_html_page(title: str, content: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='UTF-8'>
                <title>{title}</title>
            </head>
            <body>
                <header>
                    <h1>{title}</h1>
                </header>
                <main>
                    {content}
                </main>
            </body>
        </html> 
        """


@csrf_exempt
def remove(request):
    sql_delete = """DELETE FROM ex06_movies WHERE title=%s;"""
    sql_select = """SELECT * FROM ex06_movies;"""

    conn = get_connection()
    if not conn:
        return HttpResponse("Error to connected to database!")
    content = ""
    try:
        if request.method == 'POST':
            movie_to_delete = request.POST.get('title')
            if movie_to_delete:
                with conn.cursor() as cursor:
                    cursor.execute(sql_delete, (movie_to_delete,),)
                conn.commit()
            
        with conn.cursor() as cursor:
            cursor.execute(sql_select)
            movies = cursor.fetchall()
            movie = [mv[1] for mv in movies]
            content += "<form method='post'>"
            content += "<select name='title'>"
            for mov in movie:
                content += f"<option value='{mov}'>{mov}</option>"
            content += "</select>"
            content += "<button type='submit'>Delete</button></form>"
        full_page = render_html_page("Delete Movies", content)
        return HttpResponse(full_page)
    except Exception as error:
        return HttpResponse(f"Error: {error}")
    finally:
        conn.close() 

@csrf_exempt
def update(request):
    sql_update = """ 
        UPDATE ex06_movies SET opening_crawl=%s WHERE title=%s; 
        """
    sql_select = """
            SELECT * FROM ex06_movies;
        """
    conn = get_connection()
    if not conn:
        return HttpResponse("Error to connected in database!")
    content = ""
    try:
        if request.method == "POST":
            title = request.POST.get('title')
            opening_crawl = request.POST.get('opening_crawl')
            with conn.cursor() as cursor:
                cursor.execute(sql_update, (opening_crawl, title))

            conn.commit()
        
        with conn.cursor() as cursor:
            cursor.execute(sql_select)
            movies = cursor.fetchall()
            if not movies:
                return HttpResponse("Not available data!")
            movie = [mov for mov in movies]
            content = "<form method='post'><select name='title'>"
            for mov in movie:
                content += f"<option value='{mov[1]}'>{mov[1]}</option>"
            content += "</select><br><br>"
            content += "<textarea name='opening_crawl' rows='5' cols='25' placeholder='write a descriptin about the movie'></textarea><br><br>"
            content += "<button type='submit'>Update</button></form>"
        full_page = render_html_page("Update Movie", content)
        return HttpResponse(full_page)
    except Exception as error:
        return HttpResponse(f"Error: {error}")