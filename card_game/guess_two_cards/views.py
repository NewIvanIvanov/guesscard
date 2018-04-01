# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from models.users import *


def guess_game(request, cards_number):
    return render(request, 'game.html', {'cards_number': cards_number})


def menu_page(request):
    return render(request, 'index.html', )


def get_score(request):
    winner_id = User.objects.get(username=request.user)
    desk_size = request.POST.get('cardsNumber')
    high_score = request.POST.get('score')
    end_of_round = datetime.now()

    score = HighScore(username=winner_id, score=high_score,
                      score_date=end_of_round, guess_desk_number=desk_size)
    score.save()

    return JsonResponse({}, safe=False)


def score_table(request):
    score = HighScore()
    data = score.get_score_data()
    return render(request, 'score_table.html', {'data': data})
