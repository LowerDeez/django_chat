from django.contrib import admin
from chat_api.models import Room, Message


class RoomAdmin(admin.ModelAdmin):
    list_display = ['chat_type', 'label']
    list_filter = ['chat_type', ]
    readonly_fields = ['chat_type', 'label', 'members', 'last_time']


admin.site.register(Room, RoomAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'owner', 'message']
    search_fields = ['message', ]
    readonly_fields = ['message', 'owner', 'room']


admin.site.register(Message, MessageAdmin)
