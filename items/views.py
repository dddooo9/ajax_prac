from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse 
from django.template.loader import render_to_string
import json


def main(request):
    items = Post.objects.all()
    return render(request, 'items/home.html', {'items':items})

def new(request):
    return render(request, 'items/new.html')

def create(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        user = request.user
        Post.objects.create(title=title, content=content, image=image,user=user)
    return redirect('main')

def show(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.view_count = post.view_count+1
    user = request.user
    post.save()
    context = {
    'post':post,
    'user':user,
    'comments': post.comments.all().order_by('-created_at')
    }
    return render(request, 'items/show.html', context)


#삭제하기
def delete(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('main')

@require_POST
@login_required
def like_toggle(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    post_like,post_like_created = Like.objects.get_or_create(user=request.user, post=post)

    if not post_like_created:
        post_like.delete()
        result="like_cancel"
    else:
        result="like"
    context={
        "like_count":post.like_count,
        "result":result
    }
    return HttpResponse(json.dumps(context),content_type="application/json")

@require_POST
@login_required
def dislike_toggle(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    post_dislike,post_dislike_created = Dislike.objects.get_or_create(user=request.user, post=post)

    if not post_dislike_created:
        post_dislike.delete()
        result="dislike_cancel"
    else:
        result="dislike"
    context={
        "dislike_count":post.dislike_count,
        "result":result
    }
    return HttpResponse(json.dumps(context),content_type="application/json")

@login_required
@require_POST
def create_comment(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    content = request.POST.get('content')
    comment = Comment.objects.create(writer=user, post=post, content=content)
    rendered = render_to_string('comments/_comment.html', { 'comment': comment, 'user': request.user})
    context = {
		'comment': rendered
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


def delete_comment(request, comment_id):
    user = request.user
    comment=get_object_or_404(Comment,pk=comment_id)
    rendered = render_to_string('comments/_comment.html', { 'comment': comment, 'user': request.user})
    context={
        'comment': rendered
    }
    return HttpResponse(json.dumps(context), content_type="application/json")