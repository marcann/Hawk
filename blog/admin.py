from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'published_date', 'author')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.filter(author=user)

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PostAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user != obj.author:
            return False
        return True

admin.site.register(Post, PostAdmin)
