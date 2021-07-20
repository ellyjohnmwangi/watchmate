from django.urls import path
from .views import *
urlpatterns = [
    path('list/', movies_list, name='movie-list'),
    path('<int:pk>', movie_details, name='movie-detail'),
]
