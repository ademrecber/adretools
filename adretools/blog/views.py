from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import BlogPost

def blog_home(request):
    category = request.GET.get('category')
    posts = BlogPost.objects.filter(is_published=True)
    
    if category:
        posts = posts.filter(category=category)
    
    featured_posts = posts.filter(is_featured=True)[:3]
    recent_posts = posts[:10]
    
    categories = BlogPost.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    
    context = {
        'posts': recent_posts,
        'featured_posts': featured_posts,
        'categories': categories,
        'current_category': category,
        'meta_title': 'AdreTools Blog - Online Tools Guides & Tutorials',
        'meta_description': 'Comprehensive guides and tutorials for PDF tools, QR generators, calculators, and more. Learn to use digital tools effectively with expert tips.',
        'meta_keywords': 'online tools tutorials, PDF tools guide, QR code generator, calculator tools, digital tools tips, web tools tutorials'
    }
    return render(request, 'blog/home.html', context)

def blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    BlogPost.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(slug=slug)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'meta_title': post.get_og_title(),
        'meta_description': post.meta_description,
        'meta_keywords': post.meta_keywords,
        'og_title': post.get_og_title(),
        'og_description': post.get_og_description(),
        'og_image': post.featured_image,
    }
    return render(request, 'blog/post.html', context)