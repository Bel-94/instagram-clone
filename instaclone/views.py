
from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.

def welcome(request):
    return HttpResponse('Welcome to my insta clone')