# -*- coding: utf-8 -*-
import datetime

from django.db import models


class Newsmaker(models.Model):
    name = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    about = models.TextField(null=True)
    fb_id = models.CharField(max_length=255, unique=True)

    class Meta():
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __unicode__(self):
        return self.name


class Post(models.Model):

    post_types = (
        ('link', 'link'),
        ('status', 'status'),
        ('photo', 'photo'),
        ('video', 'video'),
    )

    author = models.ForeignKey(Newsmaker, db_index=True)

    fb_id = models.CharField(max_length=255, unique=True)
    header = models.TextField(default='', null=True)
    message = models.TextField(default='')
    link = models.URLField(null=True, default='')
    updated_time = models.DateTimeField(default=datetime.datetime.now())
    post_type = models.CharField(choices=post_types, max_length=6)

    like_count = models.PositiveIntegerField(default=0)
    repost_count = models.PositiveIntegerField(default=0)

    class Meta():
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __unicode__(self):
        return self.message[:23] + u' …'