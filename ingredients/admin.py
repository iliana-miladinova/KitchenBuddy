from django.contrib import admin
from .models import Ingredient
from substitutionIngredients.admin import SubstituteInline
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'category')


class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    model = Ingredient
    list_display = ('name', 'category')  
    list_filter = ('category',)          
    search_fields = ('name',)            
    ordering = ('category', 'name')
    inlines = [SubstituteInline,]

admin.site.register(Ingredient, IngredientAdmin)

