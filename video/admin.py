from django.contrib import admin
from .models import User, Jwt_token, Video

admin.site.register(User)
admin.site.register(Jwt_token)
admin.site.register(Video)