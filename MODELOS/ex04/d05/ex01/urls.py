from django.urls import path
from . import views

urlpatterns = [
            path('', views.home_page, name="home_page"),
            path('django/', views.django_page, name="django_page"),
            path('display/', views.display_pag, name="display_page"),
            path('templates/', views.templates_pag, name="templates_page")
            ]