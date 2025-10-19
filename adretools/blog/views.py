from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_home(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog/home.html', {'posts': posts})

def blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'blog/post.html', {'post': post})