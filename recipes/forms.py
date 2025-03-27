from django import forms
from .models import Tag, Recipe, MealPlan
from django.contrib.auth import get_user_model
from django.db.models import Q  

User = get_user_model()

class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Recipe
        fields = ["title", "ingredients", "instructions", "tags"]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 3}),
            "instructions": forms.Textarea(attrs={"rows": 5}),
        }

class MealPlanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show recipes belonging to the current user
            self.fields['recipe'].queryset = Recipe.objects.filter(user=user)
            # Set default date to today
            self.fields['date'].initial = forms.DateInput().value_from_datadict(
                {'date': 'today'}, {}, 'date'
            )

    class Meta:
        model = MealPlan
        fields = ['recipe', 'day', 'date']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control datepicker'
            }),
            'recipe': forms.Select(attrs={
                'class': 'form-control select2-search',
                'data-placeholder': 'Search recipes...'
            }),
            'day': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
