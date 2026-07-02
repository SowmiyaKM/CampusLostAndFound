from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import LostItem, FoundItem, Notification

User = get_user_model()


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'date_lost', 'status', 'owner', 'created_at')
    list_filter = ('category', 'status', 'date_lost')
    search_fields = ('title', 'description', 'location', 'owner__username')
    list_editable = ('status',)
    actions = ['mark_as_found', 'delete_selected']
    date_hierarchy = 'created_at'

    def mark_as_found(self, request, queryset):
        updated = queryset.update(status='found')
        self.message_user(request, f'{updated} item(s) marked as found.')
    mark_as_found.short_description = "Mark selected lost items as found"


@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'date_found', 'status', 'finder', 'created_at')
    list_filter = ('category', 'status', 'date_found')
    search_fields = ('title', 'description', 'location', 'finder__username')
    list_editable = ('status',)
    actions = ['mark_as_returned']
    date_hierarchy = 'created_at'

    def mark_as_returned(self, request, queryset):
        updated = queryset.update(status='returned')
        self.message_user(request, f'{updated} item(s) marked as returned.')
    mark_as_returned.short_description = "Mark selected found items as returned"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'notif_type', 'is_read', 'created_at')
    list_filter = ('notif_type', 'is_read')
    search_fields = ('user__username', 'message')


admin.site.site_header = "CampusConnect Administration"
admin.site.site_title = "CampusConnect Admin"
admin.site.index_title = "Lost & Found Management"
