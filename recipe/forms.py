from django import forms
from .models import IngredientsDetails

class IngredientsDetailsForm(forms.ModelForm):
    class Meta:
        model = IngredientsDetails
        fields = ['ingredient', 'quantity', 'amount']