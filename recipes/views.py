from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe, MealPlan
from .forms import RecipeForm, MealPlanForm
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.db.models import QuerySet

@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(user=request.user)

    if request.headers.get("HX-Request"):
        return render(
            request, "recipes/partials/recipe_list.html", {"recipes": recipes}
        )

    return render(request, "recipes/list.html", {"recipes": recipes})


@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()
            return redirect("recipes:list")
    else:
        form = RecipeForm()
    return render(
        request, "recipes/form.html", {"form": form, "title": "Create Recipe"}
    )


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    return render(request, "recipes/detail.html", {"recipe": recipe})


@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipes:detail", pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(
        request, "recipes/form.html", {"form": form, "title": "Update Recipe"}
    )


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == "POST":
        recipe.delete()
        return redirect("recipes:list")
    return render(request, "recipes/confirm_delete.html", {"recipe": recipe})


@login_required
def meal_plan(request):
    if request.method == "POST":
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            meal_plan.save()
            return redirect("recipes:meal_plan")
    else:
        form = MealPlanForm(user=request.user)

    # Show current week's meal plan
    meal_plans = MealPlan.objects.filter(user=request.user).order_by("date")
    return render(
        request, "recipes/meal_plan.html", {"form": form, "meal_plans": meal_plans}
    )



@login_required
def recipe_search_api(request: HttpRequest) -> JsonResponse:
    query = request.GET.get("q", "")
    # recipes = Recipe.objects.filter(user=request.user)
    recipes: QuerySet[Recipe] = Recipe.objects.filter(user=request.user)

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query)
            | Q(ingredients__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

    data = [
        {
            "id": recipe.id,
            "title": recipe.title,
            "tags": [tag.name for tag in recipe.tags.all()],
            "url": recipe.get_absolute_url(),
        }
        for recipe in recipes
    ]

    return JsonResponse({"results": data})


@login_required
def meal_plan_delete(request, pk):
    meal_plan = get_object_or_404(MealPlan, pk=pk, user=request.user)
    if request.method == "POST":
        meal_plan.delete()
    return redirect("recipes:meal_plan")
