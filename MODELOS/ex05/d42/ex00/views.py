from django.shortcuts import render
from django.http import HttpResponse
import psycopg2

# Create your views here.
def get_coonection():
    try:
        return psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            port=5432,
            host="localhost",
        )
    except psycopg2.OperationalError as error:
        print(f"Erro de conexação: {error}")
        return None


def init(request):
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
                    );"""
                ) 
        return HttpResponse("Ok")
    except Exception as e:
        return HttpResponse(f"An error occured: {e}")