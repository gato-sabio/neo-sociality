# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect

from neo_facebook.models import Post, Newsmaker
from neo_core.models import *


def raw_feed_update():
    pass


def test():
    news = Post.objects.get(pk=2)
    print news
    raw_feed = RawFeed(feed=news)
    raw_feed.save()


def add_db_post_to_raw_feed(db_post):
    new_raw_feed = RawFeed(feed_object=db_post, feed_type=db_post.post_type, item_id=db_post.id)
    new_raw_feed.save()
    return new_raw_feed


def get_recent_items_from_raw_feed(items_number):
    recent_feeds = RawFeed.objects.order_by('-id')[:items_number]
    feed_list = [feed_item.feed_object.__dict__ for feed_item in recent_feeds]
    return feed_list


def show_feed(request):
    feed_list = get_recent_items_from_raw_feed(30)
    authors = {newsmaker.id: newsmaker.name for newsmaker in Newsmaker.objects.all()}
    for feed_item in feed_list:  # подменяет id автора именем
        author_id = feed_item['author_id']
        author = authors[author_id]
        feed_item['author_id'] = author

    return render(request, 'feed.html',
        {
            'feed_list': feed_list,
        })