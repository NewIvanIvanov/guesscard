"""Custom models."""

from datetime import datetime

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
        """Get top 10 score data for each desk in one dict."""

        scores_for_12_desk = HighScore.objects.filter(
            guess_desk_number=12).order_by('score', '-score_date')[:10]
        scores_for_18_desk = HighScore.objects.filter(
            guess_desk_number=18).order_by('score', '-score_date')[:10]
        scores_for_24desk = HighScore.objects.filter(
            guess_desk_number=24).order_by('score', '-score_date')[:10]
        data = {
            'twelve': scores_for_12_desk,
            'eighteen': scores_for_18_desk,
            'twenty_four': scores_for_24desk,
        }
        return data

    def save_if_record(self, request):
        """Check record score before saving to database."""

        high_score = request.POST.get('score')
        desk_size = request.POST.get('cardsNumber')
        end_of_round = datetime.now()

        all_scores = HighScore.objects.filter(guess_desk_number=desk_size)
        if request.user.is_authenticated():
            if all_scores.count() < 10:
                self.save_winner(request, high_score, end_of_round, desk_size)
                return True
            else:
                last_score = all_scores.order_by('score', '-score_date')[9]
                if int(high_score) <= last_score.score:
                    self.save_winner(request, high_score,
                                     end_of_round, desk_size)
                    last_score.delete()
                    return True
        return False

    def save_winner(self, request, high_score, end_of_round, desk_size):
        """Save record to database."""

        winner_name = User.objects.get(username=request.user)
        score = HighScore(username=winner_name, score=high_score,
                          score_date=end_of_round, guess_desk_number=desk_size)
        score.save()

    def __unicode__(self):
        return u'{0}'.format(self.score)

    class Meta:
        managed = True
