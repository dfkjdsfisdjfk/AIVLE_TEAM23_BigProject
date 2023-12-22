from django.shortcuts import render
from django.http import HttpResponse

def test1(request):
    tmp_list = [{'name':[1], 'content':[1]},{'name':[2], 'content':[2]},{'name':[3], 'content':[3]}]
    
    return render(request, 'community/community.html', {'tmp_list':tmp_list})
