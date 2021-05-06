from django.urls import path
from watchlist_app.api.views import *

urlpatterns = [
    path('list/', WatchlistView.as_view(), name='movie-list'),
    path('platform/', StreamPlatformView.as_view(), name='platform-list'),
    path('<int:pk>', WatchlistDetailView.as_view(), name='movie-details'),
    path('platform/<int:pk>', StreamPlatformDetail.as_view(), name='platform-details')

]
