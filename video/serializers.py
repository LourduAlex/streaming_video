from rest_framework import serializers
from .models import  User, Video


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.get('password', None)
        instance = self.Meta.model(**validated_data)
        print('instance',instance)
        if password is not None:
            # instance.set_password(password)
            instance.save()
            return instance

class VideoSerializer(serializers.ModelSerializer):
    uname = serializers.CharField(sources=User.username())
    class Meta:
        model = Video
        fields = ['uname', 'name','video_url','created_at']

