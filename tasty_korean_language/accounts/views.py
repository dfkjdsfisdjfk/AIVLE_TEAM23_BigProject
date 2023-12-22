from django.shortcuts import render

def login(request):
    return render(request, 'registration/login.html')

def signup1(request):
    return render(request, 'registration/signup1.html')

def signup2(request):
    return render(request, 'registration/signup2.html')