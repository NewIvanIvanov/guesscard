from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Base user"""
    username = models.TextField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'auth_user'


class HighScore(models.Model):
    """Base model for high score table."""
    username = models.ForeignKey('User', blank=False, null=False)
    score = models.IntegerField(blank=False, null=False)
    score_date = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    guess_desk_number = models.IntegerField(blank=False, null=False)

    class Meta:
        managed = True

