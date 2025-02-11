from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Показва тези полета в списъка
    list_filter = ('category',)          # Добавя филтър по категория
    search_fields = ('name',)            # Добавя търсачка по име
    ordering = ('category', 'name')