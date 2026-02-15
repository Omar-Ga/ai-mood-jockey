from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    preview_url = models.URLField()
    jamendo_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class MoodPlaylist(models.Model):
    user_input = models.TextField()
    detected_mood = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return f"Playlist for '{self.detected_mood}' ({self.created_at})"
