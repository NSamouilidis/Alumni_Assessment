from django.contrib import admin
from .models import School, AlumniProfile, Event

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'alumni_count')
    search_fields = ('name',)
    
    def alumni_count(self, obj):
        return obj.alumni.count()
    alumni_count.short_description = 'Number of Alumni'

class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_email', 'school', 'status', 'graduation_year')
    list_filter = ('status', 'school', 'graduation_year')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_per_page = 20
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Name'
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_past_event', 'attendee_count')
    list_filter = ('date', 'registration_required')
    search_fields = ('title', 'description', 'location')
    
    def attendee_count(self, obj):
        return obj.attendees.count()
    attendee_count.short_description = 'Number of Attendees'

# Register models
admin.site.register(School, SchoolAdmin)
admin.site.register(AlumniProfile, AlumniProfileAdmin)
admin.site.register(Event, EventAdmin)