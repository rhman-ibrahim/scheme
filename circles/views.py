from django.shortcuts import render, redirect
from user.decorators import authenticated
from django.contrib import messages

from user.models import Account


@authenticated(True)
def index(request):
    return render(request, "circles/index.html")