from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured', 'view_count', 'created_at']
    list_filter = ['is_published', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'meta_keywords']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'author', 'category')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords', 'og_title', 'og_description', 'featured_image'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_published', 'is_featured', 'read_time')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.og_title:
            obj.og_title = obj.title
        if not obj.og_description:
            obj.og_description = obj.meta_description
        super().save_model(request, obj, form, change)