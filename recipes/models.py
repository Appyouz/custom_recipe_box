from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MealPlan(models.Model):
    DAY_CHOICES = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date', 'day')

    def __str__(self):
        return f"{self.date} ({self.get_day_display()}): {self.recipe.title}"
