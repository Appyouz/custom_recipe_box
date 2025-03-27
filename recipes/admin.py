from django.contrib import admin
from .models import Recipe, Tag, MealPlan

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('tags', 'created_at')
    search_fields = ('title', 'ingredients')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 'day', 'user', 'recipe')
    list_filter = ('day', 'date')
