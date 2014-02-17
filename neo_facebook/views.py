# -*- coding: utf-8 -*-

import urllib2
import json
import re
import dateutil.parser
import time

from neo_facebook.models import Newsmaker, Post
from neo_sociality.passwords import FB_APP_ID, FB_APP_SECRET
from django.http import HttpResponse
from tasks import queue_update

from neo_core.views import add_db_post_to_raw_feed

# новый токен берем на https://developers.facebook.com/tools/explorer
# HTTPError: HTTP Error 404: Not Found обычно означает, что токен просрочился
access_token = None


def load_fb_graph_in_json(url_string, options_tuple, silent=True):
    url_string_with_args = url_string.format(*options_tuple)
    if not silent:
        print '[>] Loading from URL', url_string_with_args
    try:
        result = urllib2.urlopen(url_string_with_args)
        contents = result.read()
        contents = json.loads(contents)
        if not silent:
            print '[>] URL loaded OK'
        return contents
    except urllib2.HTTPError, error:
        print '[!] Failed to load URL provided with error [{}/{}], check if access_token is up to date'.format(error.code, error.msg)


def get_access_token():
    url = 'https://graph.facebook.com//oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(FB_APP_ID, FB_APP_SECRET)
    result = urllib2.urlopen(url).read()
    access_token = result.lstrip('access_token=')
    print '[>] New App Access Token is', access_token
    return access_token

access_token = get_access_token()


def get_newsmaker_id_by_username(username):
    print '[>] Getting newsmaker id by username'
    contents = load_fb_graph_in_json('https://graph.facebook.com/{0}?access_token={1}', (username, access_token))
    user_id = contents['id']
    print '[>] [{}] id is [{}]'.format(username, user_id)
    return user_id


def precisely_count_likes(fb_post_id):
    contents = load_fb_graph_in_json('https://graph.facebook.com/{}/likes?access_token={}&limit=1&summary=1', (fb_post_id, access_token))
    likes_count = contents['summary']['total_count']
    return likes_count


def create_new_newsmaker(username):
    """ Создает новую группу для отслеживания ее новостей по username (e.g. https://www.facebook.com/alanismorissette) """

    newsmaker_id = get_newsmaker_id_by_username(username)

    contents = load_fb_graph_in_json('https://graph.facebook.com/{0}?access_token={1}', (newsmaker_id, access_token))
    newsmakers_in_db = [newsmaker.fb_id for newsmaker in Newsmaker.objects.all()]

    if contents and contents['id'] not in newsmakers_in_db:
        new_newsmaker = Newsmaker()
        try:
            new_newsmaker.name = contents['name']
        except KeyError:
            pass
        try:
            new_newsmaker.username = contents['username']
        except KeyError:
            pass
        try:
            new_newsmaker.fb_id = contents['id']
        except KeyError:
            pass
        try:
            new_newsmaker.about = contents['about']
        except KeyError:
            pass  # запишется null
        new_newsmaker.save()
        print '[>] New newsmaker created: [{}]'.format(new_newsmaker.username)
        return new_newsmaker
    else:
        print '[!] Newsmaker either in DB or do not exist'
        return None


def text_prettify(text):
    if text is None:
        return None
    text = re.sub('[\n\r\t]', ' ', text)
    text = re.sub('[ ]+', ' ', text)
    text = re.sub('-+->', '->', text)
    text = re.sub('\.\.+', u'…', text)
    text = re.sub(' - ', u' — ', text)
    return text


def choose_content(fb_post):
    """
    Находим, какие ключи из списка всех ключей FB-поста пригодны для составления текста новости
    Если среди них не только name, он пойдет в заголовок новости, а в текст пойдет самый длинный текст по прочим ключам
    Если только name, он пойдет в текст новости

    """
    output = {'header': None, 'text': None}
    actual_keys = fb_post.keys()
    desired_keys = ['message', 'story', 'description', 'name']
    keys_intersection = list(set(actual_keys).intersection(set(desired_keys)))
    # print keys_intersection
    # print type(keys_intersection)
    if 'name' in keys_intersection and len(keys_intersection) > 1:
        output['header'] = text_prettify(fb_post['name'])
        keys_intersection.remove('name')
        # print keys_intersection
        texts = [fb_post[key] for key in keys_intersection]
        output['text'] = text_prettify(max(texts))
    elif 'name' not in keys_intersection and keys_intersection:
        texts = [fb_post[key] for key in keys_intersection]
        output['text'] = text_prettify(max(texts))
    elif 'name' in keys_intersection and len(keys_intersection) <= 1:
        output['text'] = text_prettify(fb_post['name'])
    return output


def add_post_to_raw_feed(create_db_post):
    def wrapper(fb_post, author, newsmaker_id):
        new_db_post = create_db_post(fb_post, author, newsmaker_id)
        add_db_post_to_raw_feed(new_db_post)
        return new_db_post
    return wrapper


@add_post_to_raw_feed
def create_db_post(fb_post, author, newsmaker_id):
    """ Создает db_post с некоторыми обязательными полями """
    # print '[+] Creating new post in db'
    db_post = Post()
    db_post.author = author
    db_post.post_type = fb_post['type']
    db_post.fb_id = fb_post['id']
    db_post.updated_time = fb_post['updated_time']
    if 'link' in fb_post.keys():
        db_post.link = fb_post['link']
    if 'likes' in fb_post.keys():
        db_post.like_count = len(fb_post['likes']['data'])
        if db_post.like_count > 24:
            db_post.like_count = precisely_count_likes(fb_post['id'])
    if 'shares' in fb_post.keys():
        db_post.repost_count = fb_post['shares']['count']
    content = choose_content(fb_post)
    db_post.header = content['header']
    db_post.message = content['text']
    db_post.save()
    return db_post


def get_list_of_keys(fb_post):
    return [key for key in fb_post.keys()]


def load_newsmaker_posts_into_db(newsmaker, days_back=5000):
    """
    Получает в качестве аргумента id группы/пользователя и записывает в базу их новые посты без повторов

    """
    print '[>] Loading fb posts by [{}] [{}] days back'.format(newsmaker, days_back)
    since_time = int(time.time() - days_back * 86400)
    newsmaker_fb_id = newsmaker.fb_id
    contents = load_fb_graph_in_json('https://graph.facebook.com/{0}/posts?access_token={1}&limit=100&since={2}',
                                     (newsmaker_fb_id, access_token, since_time))
    fb_posts = contents['data']  # это посты, пришедшие из fb
    print '[>] FB graph loaded OK'

    author = Newsmaker.objects.get(fb_id=newsmaker_fb_id)  # группа, автор постов
    newsmaker_posts_in_db = Post.objects.filter(author=author)  # посты автора из базы

    print '[>] Starting db population'
    for fb_post in fb_posts:  # перебираем fb посты
        db_post = newsmaker_posts_in_db.filter(fb_id=fb_post['id'])  # пытаемся получить из списка постов автора готовый db пост по id
        if db_post:
            db_post = db_post[0]
            print '  [^] Post [{}] already in DB,'.format(db_post),
            post_has_updated = db_post.updated_time < dateutil.parser.parse(fb_post['updated_time'])
            if post_has_updated:
                print 'but has recently changed'
            else:
                print 'no updates found,',
        if (db_post and post_has_updated) or not db_post:  # если такого нет или такой есть, но он обновился, перезаписываем
            operation_flag = 'created'
            operation_sign = '+'
            if db_post:
                db_post.delete()
                operation_flag = 'updated'
                operation_sign = '^'
            db_post = create_db_post(fb_post, author, newsmaker_fb_id)
            print u'  [{}] Post [{}] {} OK'.format(operation_sign, db_post, operation_flag)
        else:  # если такой есть, но не обновился, обновляем счетчики репостов и лайков
            if 'shares' in fb_post.keys():
                db_post.repost_count = fb_post['shares']['count']
            if 'likes' in fb_post.keys():
                db_post.like_count = len(fb_post['likes']['data'])
                if db_post.like_count > 24:
                    db_post.like_count = precisely_count_likes(fb_post['id'])
            print 'shares/likes updated OK'
    print '[>] DB populated OK'


def load_newsmaker_posts_into_db_by_username(username, days_back):
    try:
        newsmaker = Newsmaker.objects.get(username=username)
        load_newsmaker_posts_into_db(newsmaker, days_back)
    except Newsmaker.DoesNotExist:
        return '[!] Failed to find newsmaker by the [username] provided'


def run_news_update(days_back):
    """
    :param days_back: days back to update news for
    :type days_back: int
    :returns: nothing
    :rtype: None
    """
    newsmakers = Newsmaker.objects.all()
    for newsmaker in newsmakers:
        print '[> Q] Updating', newsmaker
        queue_update.delay(newsmaker, days_back)
        print '[Q >] [{}] updated OK'.format(newsmaker)
    print '[> Q] All items in queue'


###### VIEWS #######


def test_suite(request):
    return HttpResponse('test server working…')