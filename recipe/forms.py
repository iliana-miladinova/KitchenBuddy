from django import forms
from .models import IngredientsDetails
from ingredients.models import Ingredient

class IngredientsDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.all().order_by('category', 'name')

        
    class Meta:
        model = IngredientsDetails
        fields = ['ingredient', 'quantity', 'amount']