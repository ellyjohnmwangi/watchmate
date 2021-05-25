from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase', password='Newpassword@123')
        self.token = Token.objects.get(user__username='testcase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='just netflix and chill',
                                                           website='https://netflix.com')

    def test_stream_platform_create(self):
        data = {
            'name': 'Teststream',
            'about': 'lorem ipsum dolor sit amet, consectuer',
            'website': "https://teststream.com"
        }
        response = self.client.post(reverse('platform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_deatil(self):
        response = self.client.get(reverse('platform-details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatfrom_put(self):
        data = {
            'name': 'primevideos',
            'about': 'updated woooooo',
            'website': 'https://prime.com'

        }
        response = self.client.post(reverse('platform-details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_delete(self):
        response = self.client.post(reverse('platform-details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchlistTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase2', password='Newpassword@123')
        self.token = Token.objects.get(user__username='testcase2')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='just netflix and chill',
                                                           website='https://netflix.com')
        self.watchlist = models.Watchlist.objects.create(title='testmovie', description='lorem ipsum dolor sit amet',
                                                         platform=self.stream, active=True)

    def test_watchlist_create(self):
        data = {
            'title': 'testmovie',
            'description': 'this is a test movie',
            'platform': self.stream,
            'active': False
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_details(self):
        response = self.client.get(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Watchlist.objects.count(), 1)
        self.assertEqual(models.Watchlist.objects.get().title, 'testmovie')

    def test_watchlist_put(self):
        data = {
            'title': 'testmovie1324',
            'description': 'this is 4223a test movie',
            'platform': 'Netflix',
            'active': False
        }
        response = self.client.post(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_delete(self):
        response = self.client.post(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase3', password='Newpassword@123')
        self.token = Token.objects.get(user__username='testcase3')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='just netflix and chill',
                                                           website='https://netflix.com')
        self.watchlist = models.Watchlist.objects.create(title='testmovie', description='lorem ipsum dolor sit amet',
                                                         platform=self.stream, active=True)
        self.watchlist2 = models.Watchlist.objects.create(title='testmovie2', description='lorem ipsum dolor sit amet',
                                                         platform=self.stream, active=True)

        self.review = models.Review.objects.create(review_user=self.user, rating=4, description='very good movie',
                                                   watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'very good movie',
            'watchlist': self.watchlist,
            'active': True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        # self.assertEqual(models.Review.objects.get().rating, 4)

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reviewcreate_unauth(self):
        data = {
            'review_user': self.user,
            'rating': 4,
            'description': 'very good movie',
            'watchlist': self.watchlist,
            'active': True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reviewlist(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'very good movie',
            'watchlist': self.watchlist2,
            'active': True
        }
        response = self.client.put(reverse('review-details', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reviewdetail(self):
        response = self.client.get(reverse('review-details', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-details', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_review_list(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


