from django.shortcuts import render, redirect
from django.http import JsonResponse

from bank.blog.forms import BlogFormPost
from bank.models import Blog


def blog_new(request):
    if request.method == 'POST':
        form = BlogFormPost(data=request.POST)
        if form.is_valid():
            if not Blog.objects.crate_new_post(
                    post=form.cleaned_data['post'],
                    name=form.cleaned_data['name'],
                    user=request.user.id):
                    return JsonResponse({'result': False, 'errors': form.errors})
            return redirect('blog:all')
    else:
        form = BlogFormPost()
    return render(request, 'blog/new.html', context={'form': form})


def blog_edit(request, pk):
    blog_post = Blog.objects.get(pk=pk)
    data = {
        'name': blog_post.name,
        'post': blog_post.post
    }
    if request.method == "POST":
        form = BlogFormPost(request.POST)
        if form.is_valid():
            if not Blog.objects.edit_post(
                    post=blog_post,
                    name=form.cleaned_data['name'],
                    text=form.cleaned_data['post']):
                    return redirect('blog:all')
            return JsonResponse({'result': False, 'errors': form.errors})
    else:
        form = BlogFormPost(data)
    return render(request, 'blog/edit.html', {'form': form})


def blog_del(request, pk):
    Blog.objects.delete_post(post_id=pk)
    return JsonResponse({'result': True})


def blog_all(request):
    posts = Blog.objects.filter(user_id=request.user.id)
    return render(request, 'blog/all.html', context={'posts': posts})