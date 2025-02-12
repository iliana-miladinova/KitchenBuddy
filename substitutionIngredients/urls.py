from django.urls import path
from . import views

urlpatterns = [
    path('ingredient/<int:ingredient_id>/substitutes/<int:recipe_id>/', views.get_substitute_ingredients, name='show_substitutes')
]
