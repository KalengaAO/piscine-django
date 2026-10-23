from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import os
import psycopg2

# Create your views here.
def get_connect():
    conf = {
        'dbname': settings.DATABASES['default']['NAME'],
        'user': settings.DATABASES['default']['USER'],
        'password': settings.DATABASES['default']['PASSWORD'],
        'host': settings.DATABASES['default']['HOST'],
        'port': 5432,
    }
    try:
        return psycopg2.connect(**conf)
    except Exception:
        return None

def init(request):
    slq_create_table_planets = """
            CREATE TABLE IF NOT EXISTS ex08_planets(
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR(255),
                diameter INT,
                orbital_period INT,
                populations BIGINT,
                rotation_period INT,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        """
    slq_create_table_people = """
            CREATE TABLE IF NOT EXISTS ex08_people(
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INT,
                mass REAL,
                homeworld VARCHAR(64) REFERENCES ex08_planets(name)
            );
        """
    try:
        with get_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(slq_create_table_planets)
                cursor.execute(slq_create_table_people)
        return HttpResponse("Ok")
    except Exception as error:
        return HttpResponse(f"Error: {error}")

def render_html_page(title: str, content: str) -> str:
    return f"""
            <!DOCTYPE html>
            <html lang='en'>
                <meta charset='UTF-8'>
                <title>{title}</title>
            </html>
            <body>
                <header>
                    <h1>{title}</h1>
                </header>
                <main>
                    {content}
                </main>
            </body>
        """


def populate(request):
    sql_select = """
        SELECT COUNT(*) FROM ex08_planets;
        """
    conn = get_connect()
    if not conn:
        return HttpResponse(render_html_page("error page", "No available data!"))
    result = []
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_select)
            if cursor.fetchone()[0] > 0:
                return HttpResponse(f"Base de dados already is populate!")
            with open(os.path.join(settings.BASE_DIR, 'planets.csv')) as file:
               cursor.copy_from(
                file,
                'ex08_planets',
                sep='\t',
                columns=(
                    'name',
                    'climate',
                    'diameter',
                    'orbital_period',
                    'populations',
                    'rotation_period',
                    'surface_water',
                    'terrain'
                ),
                null='NULL'
               )
               if cursor.rowcount > 0:
                    result.append(f"Table ex08_planets populated!")
            with open('people.csv', 'r') as file:
                cursor.copy_from(
                    file,
                    'ex08_people',
                    sep='\t',
                    columns=(
                        'name',
                        'birth_year',
                        'gender',
                        'eye_color',
                        'hair_color',
                        'height',
                        'mass',
                        'homeworld'
                    ),
                    null='NULL'
                )
                if cursor.rowcount > 0:
                    result.append("Table ex08_poples populated!")
                    conn.commit()
        return HttpResponse(render_html_page("Populate Database", "<br>".join(result)))
    except Exception as error:
        return HttpResponse(f"Error: {error}")
    finally:
        conn.close()

def display(request):
    sql_select = """
           SELECT p.name, p.homeworld, pl.climate 
           FROM ex08_people p JOIN ex08_planets pl 
           ON p.homeworld = pl.name WHERE pl.climate 
           LIKE '%%windy%%' ORDER BY p.name ASC;
        """
    try:
        with get_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_select)
                peoples = cursor.fetchall()
                headers = cursor.description
                if not peoples:
                    return HttpResponse(f"No data available!")
                header = [head[0] for head in headers]
                table = "<table border='1' style='border-collapse: collapse; text-align: center;'><tr>"
                for head in header:
                    table += f"<th>{head}</th>"
                table += "</tr>"
                for people in peoples:
                    table += f"<tr><td>{people[0]}</td>"
                    table += f"<td>{people[1]}</td>"
                    table += f"<td>{people[2]}</td></tr>"
                table += "</table>"
        return HttpResponse(render_html_page("List of People according your homeworld!", table))
    except Exception as error:
        return (f"Error: {error}")        

