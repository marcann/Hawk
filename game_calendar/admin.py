from django.contrib import admin
from .models import Venue, Category, Event, Guest

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('name', 'author')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return Category.objects.all()
        else:
            return Category.objects.filter(author=user)

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(CategoryAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user != obj.author:
            return False
        return True

class VenueAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('name', 'author')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return Venue.objects.all()
        else:
            return Venue.objects.filter(author=user)

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(VenueAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user != obj.author:
            return False
        return True

class GuestInline(admin.TabularInline):
    model = Guest
    extra = 3
    fields = ('user', 'attending_status')

class EventAdmin(admin.ModelAdmin):
    exclude = ('author',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'date_and_time'),
        }),
        ('E-Mail', {
            'fields': ('group', 'email_subject', 'email_message'),
        }),
        ('Event Details', {
            'fields': ('venue', 'category', 'price')
        })
    )
    inlines = [GuestInline]
    list_display = ('category', 'title', 'date_and_time', 'author')
    search_fields = ('title', 'description', 'category', 'author')


class GuestAdmin(admin.ModelAdmin):
    """
    The form to add and change guest instances.
    """
    exclude = ('emailed',)
    fields = ('event', 'user', 'attending_status')
    list_display = ('user', 'attending_status')
    list_filter = ('attending_status',)
    search_fields = ('user',)


admin.site.register(Venue, VenueAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
