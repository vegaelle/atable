from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from .views import IngredientListView, IngredientDetailView, RecipeListView, RecipeDetailView


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about$', TemplateView.as_view(template_name='recipes/about.html'),
         name='about'),
    url(r'^ingredients$', IngredientListView.as_view(), name='ingredient_list'),
    url(r'^ingredients/(?P<pk>[-\w]+)$', IngredientDetailView.as_view(),
         name='ingredient_detail'),
    url(r'^recipes$', RecipeListView.as_view(), name='recipe_list'),
    url(r'^recipes/(?P<pk>[-\w]+)$', RecipeDetailView.as_view(),
         name='recipe_detail'),
    url(r'^roadmap/meal/(?P<meal_id>\d+)$', views.roadmap_meal,
         name='roadmap_meal'),
    url(r'^roadmap/session/(?P<session_id>\d+)$', views.roadmap_session,
         name='roadmap_session'),
    ]
