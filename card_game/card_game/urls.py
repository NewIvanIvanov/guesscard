"""card_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout

from guess_two_cards.views import get_score, guess_game, menu_page, score_table

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^guessgame/(?P<cards_number>[0-9]+)/$', guess_game, name='guess_game'),
    url(r'^$', menu_page, name='menu'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^getscore/$', get_score, name='get_score'),
    url(r'^scoretable/$', score_table, name='score_table'),
]
