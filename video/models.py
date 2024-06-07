
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.username
        
class Jwt_token(models.Model):
    ids = models.CharField(primary_key=True, max_length=50, null=False)
    token = models.CharField(max_length=255)
    token_name = models.CharField(max_length=255)     

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name