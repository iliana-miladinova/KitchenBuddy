from django.contrib import admin
from .models import Ingredient

# class SubstituteInline(admin.TabularInline):
#     model = Substitute
#     fk_name = 'ingredient'
#     extra = 1
#     verbose_name = 'Substitute'
#     verbose_name_plural = 'Substitutes'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Показва тези полета в списъка
    list_filter = ('category',)          # Добавя филтър по категория
    search_fields = ('name',)            # Добавя търсачка по име
    ordering = ('category', 'name')

    # inlines = [SubstituteInline,]


# @admin.register(Substitute)
# class SubstitudeAdmin(admin.ModelAdmin):
#     list_display = ('ingredient', 'substitute_ingredient')
#     list_filter = ('ingredient__category',) #ot klas ingredient v models vzima poleto category
#     search_fields = ('ingredient__name', 'substitute_ingredient__name')
#     #autocomplete_fields = ('ingredient', 'substitute_ingredient')
