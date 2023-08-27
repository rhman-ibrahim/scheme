# Django
from django.shortcuts import render, redirect
from django.contrib import messages

# Models
from team.models import Space
from ping.models import Room
from .models import Post, Comment

# Forms
from .forms import PostForm, CommentForm

# Decorators
from helpers.decorators import back

# Funtions
from helpers.functions import get_form_errors


# Create

@back
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            signal        = form.save(commit=False)
            signal.space = Space.objects.get(id=request.session.get('circle'))
            signal.user   = request.user
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else:
            get_form_errors(request, form)

@back
def create_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            signal        = form.save(commit=False)
            signal.space = Space.objects.get(id=request.session.get('circle'))
            signal.user   = request.user
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else:
            get_form_errors(request, form)

# Retieve

def retrieve_post(request, identifier):
    signal = Post.objects.get(identifier=identifier)
    return render(
        request,
        "blog/post.html",
        {
            'post': signal,
            'room': Room.objects.get(identifier=signal.identifier),
            'forms': {
                'post': PostForm(
                    initial = {
                        'parent': signal
                    }
                ),
                'comment': CommentForm(
                    initial = {
                        'post': signal
                    }
                )
            },
            'icons': {
                'left':"diversity_2",
                "right":"forum"
            }
        }
    )

def retrieve_comment(request, identifier):
    signal = Comment.objects.get(identifier=identifier)
    return render(
        request,
        "blog/comment.html",
        {
            'comment': signal,
            'room': Room.objects.get(identifier=signal.identifier),
            'forms': {
                'comment': CommentForm(
                    initial = {
                        'parent': signal.id,
                        'post': signal.post.id
                    }
                )
            },
            'icons': {
                'left':"diversity_2",
                "right":"forum"
            }
        }
    )

# Update

def update_signal_status(request, identifier):
    query = Post.objects.filter(identifier=identifier)
    if query.exsits() and query.count() == 1:
        signal = query.first()
        signal.status = False if signal.status else True
        signal.save()
        return redirect("ping:update_room_status", signal.identifier)
    else:
        messages.warning(request, "something has gone wrong")
    return redirect("blog:detail", signal.identifier)