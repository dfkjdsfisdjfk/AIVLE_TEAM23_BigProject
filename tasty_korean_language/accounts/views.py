from django.shortcuts import render

def login():
    return ('hello')

def signup1(request):
    return render(request, 'registration/signup1.html')

def signup2(request):
    return render(request, 'registration/signup2.html')