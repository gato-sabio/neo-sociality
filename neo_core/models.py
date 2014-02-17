from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class RawFeed(models.Model):
    feed_types = (
        ('link', 'link'),
        ('status', 'status'),
        ('photo', 'photo'),
        ('video', 'video'),
    )
    item_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="Type")
    item_id = models.PositiveIntegerField(blank=True, null=True, editable=True, verbose_name=u"Link")
    feed_object = generic.GenericForeignKey('item_type', 'item_id')
    feed_type = models.CharField(choices=feed_types, max_length=6)