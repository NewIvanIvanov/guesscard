"""Django views."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from models.models import HighScore


def guess_game(request, cards_number):
    """Guess cards game view."""
    desk_size = (12, 18, 24)
    if int(cards_number) not in desk_size:
        messages.warning(
            request, 'You can play only on 12, 18 and 24 cards desk.')
        return redirect('menu')
    return render(request, 'game.html', {'cards_number': cards_number})


def menu_page(request):
    """Main page view."""
    return render(request, 'index.html', )


def post_score(request):
    """Ajax score save."""
    score = HighScore()
    winner = score.save_if_record(request)
    return JsonResponse({'winner': winner}, safe=False)


def score_table(request):
    """Score tables page view."""
    score = HighScore()
    data = score.get_score_data()
    return render(request, 'score_table.html', {'data': data})
