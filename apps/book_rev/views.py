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
    context = {
        'reviews': Review.objects.all().order_by('-created_at')[:3],
        'books': Book.objects.all()
    }
    return render(request, 'book_rev/index.html', context)

def add(request):
    if request.session['current_user'] == '':
        return render(request, 'logins/index.html')
    else:
        return render(request, 'book_rev/add.html')

def create(request):
    if request.method == 'POST':
        errors = Review.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('book_rev:add'))
        else:
            book = Book.objects.filter(name = request.POST['name'])
            user = User.objects.get(id = request.session['current_user'])
            if not book:
                book = Book.objects.create(name = request.POST['name'], author = request.POST['author'])
            else:
                book = book[0]
            review = Review.objects.create(user = user, book = book, rating = request.POST['rating'], desc = request.POST['desc'])
            return redirect(reverse('book_rev:show', kwargs={'id': book.id }))
    return redirect(reverse('logins:index'))

def show(request, id):
    book = Book.objects.get(id = id)
    context = {
        'book': book,
        'reviews': book.reviews.all().order_by('-created_at')
    }
    return render(request, 'book_rev/show.html', context)

def delete(request, id):
    review = Review.objects.get(id = id)
    book_id = review.book.id
    if request.session['current_user'] == review.user.id:
        review.delete()
    return redirect(reverse('book_rev:show', kwargs={'id': book_id }))

def show_user(request, id):
    user = User.objects.filter(id = id)
    if user:
        user = user[0]
        context = {
            'user': user,
            'reviews': user.reviews.all().order_by('-created_at')
        }
        return render(request, 'book_rev/user.html', context)
    pass