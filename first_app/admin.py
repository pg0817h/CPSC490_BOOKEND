from django.contrib import admin
from first_app.models import UserProfileInfo
from first_app.models import Event, EventMember

# Register your models here.
class EventMemberAdmin(admin.ModelAdmin):
    model = EventMember
    list_display = ['event', 'user']

admin.site.register(Event)
admin.site.register(EventMember, EventMemberAdmin)


admin.site.register(UserProfileInfo)