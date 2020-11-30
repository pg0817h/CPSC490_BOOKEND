from django.contrib import admin
from first_app.models import UserProfileInfo
from first_app.models import Event, EventMember,EventOptions,EventOptions_attendee

# Register your models here.
# class EventMemberAdmin(admin.ModelAdmin):
#     model = EventMember
#     list_display = ['event', 'email']

admin.site.register(Event)
# admin.site.register(EventMember, EventMemberAdmin)
admin.site.register(EventMember)
admin.site.register(EventOptions_attendee)
admin.site.register(EventOptions)
admin.site.register(UserProfileInfo)