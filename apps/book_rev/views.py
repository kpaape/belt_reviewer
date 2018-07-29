# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Book
from .models import Review
# may not need the above import for User
import bcrypt

# import user models
from django.apps import apps
User = apps.get_model('logins.User')

# Create your views here.

def index(request):
    return render(request, 'book_rev/index.html')



    # return redirect(reverse('logins:index'))