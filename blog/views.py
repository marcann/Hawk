from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from game_calendar.models import Event
from django.views.generic.base import TemplateView

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# DONE:0 Add navigation menu bar to the site's header.
