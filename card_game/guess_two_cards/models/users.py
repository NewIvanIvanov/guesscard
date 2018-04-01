from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Base user"""

    def __unicode__(self):
        return u'{0}'.format(self.username)

    class Meta:
        managed = False
        db_table = 'auth_user'


class HighScore(models.Model):
    """Base model for high score table."""
    username = models.ForeignKey(User, blank=False, null=False)
    score = models.IntegerField(blank=False, null=False)
    score_date = models.DateTimeField(
        blank=False, null=False, auto_now_add=True)
    guess_desk_number = models.IntegerField(blank=False, null=False)

    def get_score_data(self):
        scores_for_12_desk = HighScore.objects.filter(
            guess_desk_number=12).order_by('score', 'score_date')[:10]
        scores_for_18_desk = HighScore.objects.filter(
            guess_desk_number=18).order_by('score', 'score_date')[:10]
        scores_for_24desk = HighScore.objects.filter(
            guess_desk_number=24).order_by('score', 'score_date')[:10]
        data = {
            'twelve': scores_for_12_desk,
            'eighteen': scores_for_18_desk,
            'twenty_four': scores_for_24desk,
        }
        return data

    class Meta:
        managed = True
