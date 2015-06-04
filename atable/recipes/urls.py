from django.conf.urls import url
from . import views
from .views import RecipeListView, RecipeDetailView


urlpatterns = [
    url(r'^$', RecipeListView.as_view(), name='home'), # temp
    url(r'^recipes$', RecipeListView.as_view(), name='recipe_list'),
    url(r'^recipes/(?P<pk>[-\w]+)$', RecipeDetailView.as_view(),
         name='recipe_detail'),
    url(r'^roadmap/meal/(?P<meal_id>\d+)$', views.roadmap_meal,
         name='roadmap_meal'),
    url(r'^roadmap/session/(?P<session_id>\d+)$', views.roadmap_session,
         name='roadmap_session'),
    ]
