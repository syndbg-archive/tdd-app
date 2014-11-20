import sys

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect


def login(request):
    print('login view', file=sys.stderr)
    post_assertion = request.POST['assertion']
    user = authenticate(assertion=post_assertion)
    if user:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
