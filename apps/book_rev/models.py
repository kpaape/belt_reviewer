# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from logins.models import User

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Review(models.Model):
    # user = models.ForeignKey(User, related_name='reviews')
    user = models.IntegerField()# <- placeholder id
    book = models.ForeignKey(Book, related_name='reviews')
    rating = models.IntegerField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)