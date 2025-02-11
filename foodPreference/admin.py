from django.contrib import admin
from .models import Diet, Allergy

# Register your models here.

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)