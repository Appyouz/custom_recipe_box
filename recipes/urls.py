from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path('', views.recipe_list, name='list'),
    path('create/', views.recipe_create, name='create'),
    path('<int:pk>/', views.recipe_detail, name='detail'),
    path('<int:pk>/update/', views.recipe_update, name='update'),
    path('<int:pk>/delete/', views.recipe_delete, name='delete'),
    
    path('mealplan/', views.meal_plan, name='meal_plan'),
    path('search/', views.recipe_search, name='search'),
]
