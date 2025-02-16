from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_calorie_tracker, name='list_calorie_tracker'),
    path('add/<int:recipe_id>/', views.add_to_calorie_tracker, name='add_to_calorie_tracker'),
    path('remove/<int:recipe_id>/', views.remove_from_calorie_tracker, name='remove_from_calorie_tracker'),
    path('update/<int:recipe_id>/', views.edit_servings, name='update_servings'),
]