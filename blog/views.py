# Django
from django.shortcuts import render, redirect
from django.contrib import messages

# Models
from team.models import Circle
from ping.models import Room
from .models import Post

# Forms
from .forms import PostForm

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
            signal.circle = Circle.objects.get(id=request.session.get('circle'))
            signal.user   = request.user
            try:
                signal.parent = Post.objects.get(id=request.session.get('parent_signal_id'))
            except Post.DoesNotExist:
                pass
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else:
            get_form_errors(request, form)

# Retieve

def retrieve_post(request, serial):
    signal = Post.objects.get(serial=serial)
    request.session['parent_signal_id'] = signal.id
    return render(
        request,
        "blog/index.html",
        {
            'post': signal,
            'room': Room.objects.get(serial=signal.serial),
            'forms': {
                'post':PostForm
            },
            'icons': {
                'left':"diversity_2",
                "right":"forum"
            }
        }
    )

# Update

def update_signal_status(request, serial):
    query = Post.objects.filter(serial=serial)
    if query.exsits() and query.count() == 1:
        signal = query.first()
        signal.status = False if signal.status else True
        signal.save()
        return redirect("ping:update_room_status", signal.serial)
    else:
        messages.warning(request, "something has gone wrong")
    return redirect("blog:detail", signal.serial)