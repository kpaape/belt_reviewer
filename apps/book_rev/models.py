# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logins.models import User

# Create your models here.


class ReviewManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['name']) < 1:
            errors['name'] = 'Title cannot be blank'
        if len(post_data['author']) < 1:
            errors['author'] = 'Author cannot be blank'
        if len(post_data['author']) < 1:
            errors['author'] = 'Author cannot be blank'
        if len(post_data['desc']) < 1:
            errors['desc'] = 'Review cannot be blank'
        return errors

class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews')
    # user = models.IntegerField()# <- placeholder id
    book = models.ForeignKey(Book, related_name='reviews')
    rating = models.CharField(max_length=5)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()