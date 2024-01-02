from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Post



def test1(request):
    # tmp_list = [{'name':[1], 'content':[1]},{'name':[2], 'content':[2]},{'name':[3], 'content':[3]}] * 3
    tmp_list = Post.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(tmp_list, 10)
    page = paginator.get_page(int(page))
    
    start_page = page.number // 10 * 10
    if page.number // 10 != paginator.num_pages // 10:
        last_page = start_page + 10
    else:
        last_page = start_page + paginator.num_pages % 10
    pages = [i for i in range(start_page+1, last_page+1)]
    
    contents = {
        'page_obj' : page,
        'page_paginator' : paginator,
        'pages' : pages,
    }
    
    print(Post.objects.all()[0].pk)

    
    return render(request, 'community/community.html', contents)

def posting(request, pk):
    
    post = Post.objects.get(pk=pk)
 
    return render(request, 'community/community_detail.html', {'post':post})