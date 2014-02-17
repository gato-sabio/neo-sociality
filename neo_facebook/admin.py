import models
from django.contrib import admin
from neo_facebook.models import Post, Newsmaker


# class DrugAdmin(admin.ModelAdmin):
#     list_display = ['name_rus', 'url', 'date']
#     ordering = ('-date',)
#     list_per_page = 30
#     search_fields = ['name_rus']

admin.site.register(Post)
admin.site.register(Newsmaker)
