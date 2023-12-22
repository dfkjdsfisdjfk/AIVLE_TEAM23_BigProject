from django.shortcuts import render
from django.http import HttpResponse

def test1(resquest):
    return HttpResponse('커뮤니티')
