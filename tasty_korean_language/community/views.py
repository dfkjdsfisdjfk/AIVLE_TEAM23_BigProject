from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm


def show_list(request):
    tmp_list = Post.objects.all().order_by('-create_date')
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
    
    return render(request, 'community/community_list.html', contents)

def detail(request, pk):
    
    post = Post.objects.get(pk=pk)
    print(request.user)
 
    return render(request, 'community/community_detail.html', {'post':post, 'user':request.user})


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


def update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            redirect('community:detail', pk=id)
        return redirect(post)
    else:
        form = PostForm(instance=post)
        return render(request, 'community/community_update.html', {'form':form})
    
    
def delete(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('community:index')
    else:
        return render(request, 'community/community_delete.html', {'post':post})