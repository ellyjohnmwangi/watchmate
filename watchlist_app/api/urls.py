from django.urls import path

from watchlist_app.api.views import *

urlpatterns = [
    path('list/', WatchlistView.as_view(), name='movie-list'),
    path('<int:pk>/', WatchlistDetailView.as_view(), name='movie-details'),
    path('platform/', StreamPlatformView.as_view(), name='platform-list'),
    path('platform/<int:pk>/', StreamPlatformDetail.as_view(), name='platform-details'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/reviews-create/', ReviewCreate.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-details'),
    path('reviews/', UserReview.as_view(), name='review-details2'),
    path('movies/', MovieList.as_view(), name='movies-list')

]
