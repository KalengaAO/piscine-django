from django.urls import path
from . import views

urlpatterns = [
        path('', views.search_views, name='search_viewss'),
        path('populate/', views.populate, name='populate'),
]