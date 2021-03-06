from django.db import models
from django.db.models import CharField, Model
from django_mysql.models import ListCharField



class Track(models.Model):
    track_id = models.CharField(max_length=32)
    track_artist = models.CharField(max_length=128)
    track_name = models.CharField(max_length=128)
    danceability = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    valence = models.FloatField()
    instrumentalness = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()
    key = models.FloatField(null=True)
    duration_ms = models.FloatField(null=True)
    mode = models.FloatField(null=True)
    time_signature = models.FloatField(null=True)
    loudness = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    isrc = models.CharField(max_length=32, null=True)
    like_it = models.CharField(max_length=32, null=True)
    user_id = models.CharField(max_length=32, default='')
    user_name = models.CharField(max_length=128, default='')
    popularity = models.FloatField(null=True)
    artist_id = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.track_artist + ' - ' + self.track_name


class Album(models.Model):
    album_id = models.CharField(max_length=32)
    album_artist = models.CharField(max_length=128)
    album_name = models.CharField(max_length=128)
    danceability = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    valence = models.FloatField()
    instrumentalness = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()
    upc = models.CharField(max_length=32, null=True)
    like_it = models.CharField(max_length=32, null=True)
    user_id = models.CharField(max_length=32, default='')
    user_name = models.CharField(max_length=128, default='')
    popularity = models.FloatField(null=True)
    artist_id = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.album_artist + ' - ' + self.album_name


class Artist(models.Model):
    artist_id = models.CharField(max_length=32)
    artist_name = models.CharField(max_length=128)
    followers = models.FloatField(null=True)
    popularity = models.FloatField(null=True)
    genres = ListCharField(
        base_field=models.CharField(max_length=16,null=True),
        size=32,
        max_length=(32 * 17)  # 6 * 10 character nominals, plus commas
    )
    like_it = models.CharField(max_length=32, null=True)
    user_id = models.CharField(max_length=32, default='')
    user_name = models.CharField(max_length=128, default='')
    

    def __str__(self):
        return self.artist_name        
