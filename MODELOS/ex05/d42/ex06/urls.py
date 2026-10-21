from django.urls import path
from . import views

urlpatterns = [
        path('init/', views.init, name="init"),
        path('display/', views.display, name="display"),
        path('populate/', views.populate, name='populate'),
        path('remove/', views.remove, name='remove'),
        path('update/', views.update, name='update'),
    ]