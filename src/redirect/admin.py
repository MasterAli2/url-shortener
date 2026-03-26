from django.contrib import admin
from .models import ShortLink

@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ['code', 'url', 'owner', 'created_at']
    search_fields = ['code', 'url', 'owner__username']
    list_filter = ['owner']