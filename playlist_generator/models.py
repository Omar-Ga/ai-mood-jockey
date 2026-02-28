from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    preview_url = models.URLField()
    jamendo_id = models.CharField(max_length=50, unique=True)
    album_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class MoodQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries")
    user_input = models.CharField(max_length=500)
    generated_keywords = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tracks = models.ManyToManyField(Track, related_name='mood_queries')

    def __str__(self):
        return f"Query by {self.user.username} at {self.created_at}"
