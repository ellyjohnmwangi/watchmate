from django.urls import path
from watchlist_app.api.views import *

urlpatterns = [
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetailView.as_view(), name='movie-details')
]
