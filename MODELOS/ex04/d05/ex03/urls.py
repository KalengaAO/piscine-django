from django.urls import path
from . import views 

urlpatterns = [
                path("", views.gradient_table, name="gradient")
            ]