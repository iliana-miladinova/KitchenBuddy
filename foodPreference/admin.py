from django.contrib import admin
from .models import Diet, Allergy
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class DietResource(resources.ModelResource):
    class Meta:
        model = Diet
        fields = ('id', 'name')


class DietAdmin(ImportExportModelAdmin):
    resource_class = DietResource
    model = Diet
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Diet, DietAdmin)

class AllergyResource(resources.ModelResource): 
    class Meta:
        model = Allergy
        fields = ('id', 'name')

class AllergyAdmin(ImportExportModelAdmin):
    resource_class = AllergyResource
    model = Allergy
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Allergy, AllergyAdmin)
