from django.urls import re_path
from chat_api.views import NewChatView, HomeView, ChatRoomMessagesView, ChatRoomsView


urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='main'),
    re_path(r'^chat_rooms/(?P<pk>[0-9]+)/$', ChatRoomsView.as_view(), name='chat_rooms'),
    re_path(r'^chats/get_messages/(?P<pk>[0-9]+)/$', ChatRoomMessagesView.as_view(), name='chat_get_messages'),
    re_path(r'^chats/new/(?P<room_type>[0-9]+)/$', NewChatView.as_view(), name='new_room'),
]
