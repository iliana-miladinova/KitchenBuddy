from django.urls import path
from . import views

urlpatterns =[
    path('recommend/', views.get_recipes_by_ingredients, name='get_recipes_by_ingredients'),
]