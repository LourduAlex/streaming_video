import cv2
import threading
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from .models import Video

class VideoCamera(object):
    def __init__(self, url):
        self.url = url
        self.cap = cv2.VideoCapture(url)
        (self.grabbed, self.frame) = self.cap.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        return self.frame

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.cap.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def stream_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    camera = VideoCamera(video.video_url)
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')
