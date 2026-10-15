from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import psycopg2

# Create your views here.
def get_coonection():
    try:
        return psycopg2.connect(
            dbname=settings.DATABASES.get('default', {}).get('NAME', 'testdb'),
            user=settings.DATABASES.get('default').get('USER', 'testuser'),
            password=settings.DATABASES.get('default', {}).get('PASSWORD', 'testsecret'),
            port=5432,
            host=settings.DATABASES['default']['HOST'],
        )
    except psycopg2.OperationalError as error:
        print(f"Error to connect: {error}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def init(request):
    conn = None
    try:
        with get_coonection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ex00_movies (
                        episode_nb INT PRIMARY KEY,
                        title VARCHAR(64) UNIQUE NOT NULL,
                        opening_crawl TEXT,
                        director VARCHAR(32) NOT NULL,
                        produce VARCHAR(128) NOT NULL,
                        release_data DATE NOT NULL
                    );
                    """
                )
        return HttpResponse("Ok")
    except Exception as e:
        return HttpResponse(f"An error occured: {e}")
    finally:
        if conn is not None:
            conn.close()