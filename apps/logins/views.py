# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.

def index(request):
    if not 'current_user' in request.session:
        request.session['current_user'] = ''
    if request.session['current_user'] == '':
        return render(request, 'logins/index.html')
    else:
        print "sending to book index"
        return redirect(reverse('book_rev:index'))

def submit(request):
    if request.method == 'POST':
        if request.POST['action'] == "login":
            errors = User.objects.basic_login(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect(reverse('logins:login_reg'))
            else:
                request.session['current_user'] = User.objects.get(email = request.POST['email']).id
                return redirect(reverse('book_rev:index'))
            
        if request.POST['action'] == "register":
            errors = User.objects.basic_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect(reverse('logins:login_reg'))
            else:
                hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash_pw)
                request.session['current_user'] = user.id
                return redirect(reverse('book_rev:index'))
    return redirect(reverse('logins:index'))

def all_users(request):# this is for testing purposes only
    context = {
        'users': User.objects.all()
    }
    return render(request, 'logins/all_users.html', context)

def account(request):
    if request.session['current_user'] == '':
        return redirect(reverse('logins:index'))
    else:
        context = {
            'user': User.objects.get(id = request.session['current_user'])
        }
        return render(request, 'logins/account.html', context)

def logout(request):
    request.session.clear()
    return redirect(reverse('logins:index'))