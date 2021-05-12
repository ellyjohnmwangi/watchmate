from django.urls import path, include
from watchlist_app.api.views import *
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('platform', StreamPlatformView, basename='streamplatform')

urlpatterns = [
    path('list/', WatchlistView.as_view(), name='movie-list'),
    path('<int:pk>', WatchlistDetailView.as_view(), name='movie-details'),
    # path('', include(router.urls)),
    path('platform/', StreamPlatformView.as_view(), name='platform-list'),
    path('platform/<int:pk>/', StreamPlatformDetail.as_view(), name='platform-details'),
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-details'),
    path('platform/<int:pk>/reviews/', ReviewDetailView.as_view(), name='review-list'),
    path('platform/<int:pk>/reviews-create/', ReviewCreate.as_view(), name='review-create'),
    path('platform/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-details')

]