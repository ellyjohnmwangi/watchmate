from rest_framework import status, mixins, generics, viewsets, filters
# from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.models import StreamPlatform, Watchlist
from watchlist_app.api.serializers import *
from watchlist_app.api.permission import AdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.response import Response
from watchlist_app.api.throttling import ReviewListThrottle, ReviewCreateThrottle


class UserReview(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('Already Reviewed')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    # throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review_detail'


class StreamPlatformView(generics.ListCreateAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    # def list(self, request):
    #     queryset = StreamPlatform.objects.all()
    #     serializer = StreamPlatformSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request):
    #     queryset = StreamPlatform.objects.all()
    #


class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class WatchlistView(generics.ListCreateAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer


class WatchlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer


class MovieList(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']
