from django.shortcuts import render
from django.http import HttpResponse
from .models import Planets, People
# Create your views here.

def display(request):
    try:
        if not People.objects.exists():
            return HttpResponse(f"No data \
            available, please use the following command before using this page: \
            <br><br><code>python3 manage.py loaddata ex09_initial_data.json</code>")
        people = (
                People.objects.filter(
            homeworld__climate__icontains="windy").order_by("name").select_related("homeworld")
        )
       
        content = {
            'people': people,
            'title': "List of people, climate and homeworld"
        }
        return render(request, 'ex09/index.html', content)
    except Exception as error:
        return HttpResponse(f"Error: {error}")
