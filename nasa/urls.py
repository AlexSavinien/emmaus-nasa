from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAsteroidList, name="asteroids"),
    path('asteroid/<str:id>', views.getAsteroid, name="asteroid"),

]
