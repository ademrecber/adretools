from django.db import models
from django.utils import timezone
from django.urls import reverse

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short description for blog listing")
    meta_description = models.CharField(max_length=160)
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    og_title = models.CharField(max_length=60, blank=True, help_text="Open Graph title")
    og_description = models.CharField(max_length=160, blank=True, help_text="Open Graph description")
    featured_image = models.URLField(blank=True, help_text="URL for featured image")
    author = models.CharField(max_length=100, default="AdreTools Team")
    category = models.CharField(max_length=50, choices=[
        ('tutorials', 'Tutorials'),
        ('guides', 'Guides'),
        ('tips', 'Tips & Tricks'),
        ('updates', 'Updates'),
        ('tools', 'Tool Reviews')
    ], default='guides')
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_published', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['is_featured', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:blog_post', kwargs={'slug': self.slug})
    
    def get_og_title(self):
        return self.og_title or self.title
    
    def get_og_description(self):
        return self.og_description or self.meta_description