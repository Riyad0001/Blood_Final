from django.contrib import admin
from .models import Event, Donation

class EventAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'blood_group_needed', 'created_at', 'is_active')
    list_filter = ('blood_group_needed', 'is_active')
    search_fields = ('title', 'creator__username')
    raw_id_fields = ('creator',)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'event', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('donor__username', 'event__title')
    raw_id_fields = ('donor', 'event')

admin.site.register(Event, EventAdmin)
admin.site.register(Donation, DonationAdmin)