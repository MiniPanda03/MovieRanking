# models.py

from django.contrib.auth.models import User
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'mainpage_movie'

class UserRanking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'mainpage_userranking'

class RankedMovie(models.Model):
    ranking = models.ForeignKey(UserRanking, on_delete=models.CASCADE)
    movie_id = models.IntegerField(default=0)
    position = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"Movie ID: {self.movie_id} - Position: {self.position}"
    
    class Meta:
        db_table = 'mainpage_rankedmovie'