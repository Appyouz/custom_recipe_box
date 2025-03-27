from django import forms
from .models import Tag, Recipe, MealPlan


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
    class Meta:
        model = MealPlan
        fields = ["recipe", "day", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
