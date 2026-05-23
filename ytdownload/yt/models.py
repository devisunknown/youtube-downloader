from django.db import models
from django.contrib.auth.models import User

class DownloadTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")
