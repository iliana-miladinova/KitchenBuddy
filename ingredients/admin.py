from django.contrib import admin
from .models import Ingredient
from substitutionIngredients.admin import SubstituteInline

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Показва тези полета в списъка
    list_filter = ('category',)          # Добавя филтър по категория
    search_fields = ('name',)            # Добавя търсачка по име
    ordering = ('category', 'name')
    inlines = [SubstituteInline,]

