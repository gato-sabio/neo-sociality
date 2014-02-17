# -*- coding: utf-8 -*-

# Create your views here.
from neo_facebook.models import Newsmaker, Post
from django.http import HttpResponse
from oauth_tokens import *
import urllib2
import json
from .neo_sociality import settings

# https://developers.facebook.com/tools/explorer
ACCESS_TOKEN = 'CAACEdEose0cBAFZBqJvFIViZADCoZAjXrZABwin1XKrNAtQezS7hHCyI9Ih4lBkIUs7CGH1oC1jtmAc3yunEg0l7LSHqBmo8jVCYLSyuDB0yK5v82jGmnJhRbm1khbpghinNoFd4fpNKT1XHhTc8zjrjzWyrrb3CFd07VgxsF1pNshDnEFTBIZBML4UWpe4qA4EOGnQ7IvgZDZD'


def CreateNewGroup(user_id):
    # загрузка данных и декодирование json
    url_to_group_page_with_token = 'https://graph.facebook.com/{}?access_token={}'.format(user_id, ACCESS_TOKEN)
    url_to_group_page_with_no_token = 'https://graph.facebook.com/{}'.format(user_id)

    try:
        result = urllib2.urlopen(url_to_group_page_with_token)
    except:
        result = urllib2.urlopen(url_to_group_page_with_no_token)
    print url_to_group_page_with_token
    contents = result.read()
    contents = json.loads(contents)

    # разборка json, создание новой группы
    # TODO Проверять группу на дубли
    if contents:
        new_group = Newsmaker()
        try:
            new_group.name = contents['name']
        except KeyError:
            pass
        try:
            new_group.username = contents['username']
        except KeyError:
            pass
        try:
            new_group.fb_id = contents['id']
        except KeyError:
            pass
        try:
            new_group.about = contents['about']
        except KeyError:
            pass  # запишется null
        new_group.save()


def GetUserPosts(user_id):
    """
    Получает в качестве аргумента id или имя группы/пользователя и записывает
    в базу их новые посты без повторов
    """

    ## TODO Убрать
    user_id = Newsmaker.objects.get(username='LeagueOfLegendsOceania').fb_id
    print user_id

    url_to_posts = 'https://graph.facebook.com/{}/posts?access_token={}'.format(user_id, ACCESS_TOKEN)
    contents = urllib2.urlopen(url_to_posts).read()
    print contents
    return 'done'