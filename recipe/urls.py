from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_recipe, name='list_recipe'),
    path('create/', views.recipe_create, name='recipe_create'),
    path('favourite/', views.favourite_recipes, name='favourite_recipes'),
    path('favourite/<int:recipe_id>/', views.add_remove_favourite, name='add_remove_favourite'),
    path('<int:recipe_id>/', views.recipe_details, name='recipe_details'),
    path('<int:recipe_id>/update/', views.recipe_update, name='recipe_update'),
    path('<int:recipe_id>/rate/', views.add_rating, name='add_rating'),
    path('<int:recipe_id>/comment/', views.add_comment, name='add_comment')


]