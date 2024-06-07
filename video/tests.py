from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Video

class VideoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.video = Video.objects.create(user=self.user, name='Test Video', video_url='http://example.com/video.mp4')

    def test_create_video(self):
        response = self.client.post('/api/videos', {'name': 'New Video', 'video_url': 'http://example.com/video2.mp4'})
        self.assertEqual(response.status_code, 201)

    def test_get_videos(self):
        response = self.client.get('/api/videos')
        self.assertEqual(response.status_code, 200)

    def test_search_videos(self):
        response = self.client.get('/api/videos/search?q=Test')
        self.assertEqual(response.status_code, 200)

