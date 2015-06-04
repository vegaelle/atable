from django.conf.urls import url
from . import views
from .views import RecipeListView, RecipeDetailView


urlpatterns = [
    url(r'^recipes$', RecipeListView.as_view()),
    url(r'^recipes/(?P<pk>[-\w]+)$', RecipeDetailView.as_view()),
    url(r'^roadmap/meal/(?P<meal_id>\d+)$', views.roadmap_meal,
         name='roadmap_meal'),
    url(r'^roadmap/session/(?P<session_id>\d+)$', views.roadmap_session,
         name='roadmap_session'),
    ]
