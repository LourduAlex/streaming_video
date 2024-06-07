from django.contrib import admin
from django.urls import path
from video.views import RegisterView, LoginView, CreateEditVideoView, VideoListView, DeleteVideoView, VideoSearchAPIView
from .streaming import stream_video
urlpatterns = [


    path('register/', RegisterView.as_view(), name='Register'),
    path('login/', LoginView.as_view(), name='Login'),
    path('createvideo/', CreateEditVideoView.as_view(), name='createvideo'),
    path('create/<int:id>', CreateEditVideoView.as_view(), name='editvideo'),
    path('deletevideo/<int:id>', DeleteVideoView.as_view(), name='deletevideo'),
    path('videolist/<int:id>', VideoListView.as_view(), name='videolist'),
    path('stream/<int:video_id>/', stream_video, name='stream-video'),
    path('videos/search', VideoSearchAPIView.as_view(), name='video-search'),

    
]




