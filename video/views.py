from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Jwt_token, Video
from .serializers import *
import jwt 
from rest_framework.generics import ListAPIView

class RegisterView(APIView):
    def post(self, request, format=None):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            response_data = {
                'success': True,
                'message': "Account Created Successfully",
                'userId': instance.id,
                'username': instance.username
            }
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user_exists = User.objects.filter(username=username, password=password).first()

        if user_exists is None:
            raise AuthenticationFailed({'success': 'false', 'message': 'Login Failed!'})


        payload = {
            'id': user_exists.id,
            'username': user_exists.username,
            'password': user_exists.password,
        }

        # print("user_exists.id", user_exists.id)
        token_id = user_exists.id

        token = (jwt.encode(payload, 'secret', algorithm='HS256'))
        decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = decoded_token.get('id')

        print("Login Api Used So Token ID printed :", user_id)

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        # print("token", token)

        jwt_token_instance = Jwt_token(
            ids=user_exists.id, token=token, token_name=username)
        jwt_token_instance.save()

        response.data = {
            'success': 'true',
            'message': 'login successfully ',
            'userId': user_exists.id,
            'username': user_exists.username,
            'token': token
        }

        return response
    
class CreateEditVideoView(APIView):
    
    def post(self, request, pk=None):
        if pk:
            try:
                Video_instance = Video.objects.get(pk=pk)
            except Video.DoesNotExist:
                return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = VideoSerializer(Video_instance, data=request.data)
            message_success = "Your Video has been successfully edited"
            message_failure = "Your Video cannot be edited"
        else:

            serializer = VideoSerializer(data=request.data)
            message_success = "Video has been successfully created"
            message_failure = "Video failed to create"

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': message_success,
                    'serializer': serializer.data
                })
            else:
                return Response({
                    'success': False,
                    'message': message_failure,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            

class DeleteVideoView(APIView):
    def delete(self, request, id):
        try:
            video_instance = Video.objects.get(id=id)
            Video.delete()
            return Response({
            'success': True,
            'message': "Video Deleted successfully"})
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        
class VideoListView(ListAPIView):
    serializer_class = VideoSerializer

    def list(self, request):
        id = self.request.query_params.get('id')

        if not id:
            return Response({"success": False, "message": "id is required"})


        vendorlist = Video.objects.filter(id=id)
        message = "Video List retrieved successfully from a particular vendor."

        serialized_data = self.serializer_class(vendorlist, many=True).data     

        status_code = status.HTTP_200_OK
        return Response(serialized_data, status=status_code)


class VideoSearchAPIView(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        return Video.objects.filter(name__icontains=query)