from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from django.core import serializers

from bank.blog.forms import BlogFormPost, CommentFormPost
from bank.models import Blog, Comment


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
    query_for_comments = '''SELECT bankdb."public"."user".username,
                                        bankdb."public".comment.text,
                                        bankdb."public".comment.id,
                                        bankdb."public".comment."date",
                                        bankdb."public".comment.parent_id
                                        FROM bankdb."public".comment
                                        JOIN bankdb."public"."user"
                                        ON bankdb."public"."user".id = bankdb."public".comment.user_id
                                        WHERE bankdb."public".comment.parent_id ISNULL'''
    query_for_replies = '''SELECT bankdb."public"."user".username,
                                        bankdb."public".comment.text,
                                        bankdb."public".comment.id,
                                        bankdb."public".comment."date",
                                        bankdb."public".comment.parent_id
                                        FROM bankdb."public".comment
                                        JOIN bankdb."public"."user"
                                        ON bankdb."public"."user".id = bankdb."public".comment.user_id
                                        WHERE bankdb."public".comment.parent_id IS NOT NULL '''
    posts = Blog.objects.filter(user_id=request.user.id)
    comments = Comment.objects.raw(query_for_comments)
    replies = Comment.objects.raw(query_for_replies)
    # json_posts = serializers.serialize("json", posts)
    # json_comments = serializers.serialize("json", comments)
    # json_replies = serializers.serialize("json", replies)
    # json_data_list = [json_posts, json_comments, json_replies]
    # return HttpResponse(json_data_list, content_type="application/json")
    return render(request, 'blog/all.html', context={'posts': posts,
                                                     'comments': comments,
                                                     'replies': replies})


def comment_new(request, pk):
    blog_post = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentFormPost(data=request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']
            user_id = request.user.id
            user_name = request.user.username
            post_id = blog_post.id
            new_comment = Comment.objects.create_new_comment(
                    text=comment_text,
                    user=user_id,
                    post=post_id)
            if not new_comment:
                    return JsonResponse({'result': False, 'errors': form.errors})
            return JsonResponse({'result': True, 'comment': new_comment,
                                 'text': comment_text, 'user': user_id,
                                 'user_name': user_name, 'post_id': post_id})
    else:
        form = CommentFormPost()
    return render(request, 'blog/all.html', context={'form': form})


def reply_to_comment(request, pk_post, pk_comment):
    blog_post = Blog.objects.get(pk=pk_post)
    parent = Comment.objects.get(pk=pk_comment)
    if request.method == 'POST':
        form = CommentFormPost(data=request.POST)
        if form.is_valid():
            if not Comment.objects.create_reply(
                    text=form.cleaned_data['text'],
                    user=request.user.id,
                    post=blog_post.id,
                    parent=parent.id):
                return JsonResponse({'result': False, 'errors': form.errors})
            return redirect('blog:all')
    else:
        form = CommentFormPost()
    return render(request, 'blog/all.html', context={'form': form})


def comment_del(request, pk):
    Comment.objects.delete_comment(comment_id=pk)
    return JsonResponse({'result': True})
