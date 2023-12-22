from django.shortcuts import render

def login():
    return ('hello')

def signup(request):
    return render(request, 'registration/signup.html')