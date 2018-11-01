# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Book
from .models import Review


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
        return redirect(reverse('logins:index'))
    else:
        return render(request, 'book_rev/add.html')

def create(request):
    if request.method == 'POST':
        print request.POST['name']
        context = {
            'book_name': request.POST['name'],
            'book_author': request.POST['author'],
            'book_rating': request.POST['rating'],
            'book_desc': request.POST['desc'],
        }
        print context['book_name']
        print "*-" * 20
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
    elif request.session['current_user'] == '':
        return redirect('logins:index')
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