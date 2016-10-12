from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from game_calendar.models import Event
from django.views.generic.base import TemplateView
from .forms import PostForm, PostDeleteForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.published_date = timezone.now()
        post.save()
        return HttpResponseRedirect('/')
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.created_date = timezone.now()
            new_post.save()

            return render(request, 'blog/post_detail.html', {'post': new_post})

    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post.title = post_form.cleaned_data['title']
            post.text = post_form.cleaned_data['text']
            post.save()

            return render(request, 'blog/post_detail.html', {'post': post})

    return render(request, 'blog/post_edit.html', {'post': post, 'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return HttpResponseRedirect('/')
    else:
        form = PostDeleteForm(instance=post)

    return render(request, 'blog/post_delete.html', {'form': form, 'post': post})

# DONE: Added delete view for Posts.
# DONE:20 Add navigation menu bar to the site's header.
