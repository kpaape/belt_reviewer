# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-z]+$')


class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'
        elif not NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = 'First name can only contain alphabetical characters A-Z and a-z'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        elif not NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = 'Last name can only contain alphabetical characters A-Z and a-z'
        if len(post_data['email']) < 1:
            errors['email'] = 'Email cannot be blank'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid email'
        elif User.objects.filter(email = post_data['email']):
            errors['email'] = 'The provided email is already in use'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if not post_data['password'] == post_data['confirm_password']:
            errors['confirm_password'] = 'Confirm password did not match'
        return errors

    def basic_login(self, post_data):
        errors = {}
        user = User.objects.filter(email = post_data['email'])
        if not user:
            errors['login'] = 'Incorrect credentials'
        elif not bcrypt.checkpw(post_data['password'].encode(), user[0].password.encode()):
            errors['login'] = 'Incorrect credentials'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()