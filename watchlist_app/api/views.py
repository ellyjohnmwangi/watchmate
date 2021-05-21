from rest_framework import status, mixins, generics, viewsets
# from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from watchlist_app.models import StreamPlatform, Watchlist
from watchlist_app.api.serializers import *
from watchlist_app.api.permission import AdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.response import Response


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

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
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


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
