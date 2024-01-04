from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm


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
    
    print(Post.objects.all()[0])

    
    return render(request, 'community/community.html', contents)

def posting(request, pk):
    
    post = Post.objects.get(pk=pk)
 
    return render(request, 'community/community_detail.html', {'post':post})


def write(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form_dic = form.cleaned_data
            form_dic['writer'] = request.user
            print(form.cleaned_data, request.user)
            post = Post.objects.create(**form.cleaned_data)
        return redirect(post)
    else:
        form = PostForm()

        return render(request, 'community/community_write.html', {'form':form})