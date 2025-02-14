from django.contrib import admin
from  .models import Substitute

# Register your models here.
class SubstituteInline(admin.TabularInline):
    model = Substitute
    fk_name = 'ingredient'
    extra = 1
    verbose_name = 'Substitute'
    verbose_name_plural = 'Substitutes'


class SubstitudeAdmin(admin.ModelAdmin):
    model = Substitute
    list_display = ('ingredient', 'substitute_ingredient')
    list_filter = ('ingredient__category',) #ot klas ingredient v models vzima poleto category
    search_fields = ('ingredient__name', 'substitute_ingredient__name')
    #autocomplete_fields = ('ingredient', 'substitute_ingredient')

admin.site.register(Substitute, SubstitudeAdmin)
