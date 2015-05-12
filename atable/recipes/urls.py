from django.conf.urls import url
from . import views


urlpatterns = \
    [url(r'^roadsheet/meal/(?P<meal_id>\d+)$', views.roadsheet_meal,
         name='roadsheet_meal'),
     ]
