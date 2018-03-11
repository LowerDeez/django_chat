from channels.db import database_sync_to_async
from chat_api.exceptions import ClientError
from chat_api.models import Room, Message
from django.utils import timezone


@database_sync_to_async
def get_room_or_error(room_id, user):
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    return room


@database_sync_to_async
def create_msg_or_error(room_id, user, message):
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        room = Room.objects.get(pk=room_id)
        room.last_time = timezone.now()
        room.save()
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    try:
        msg = Message()
        msg.room_id = room_id
        msg.owner_id = user.id
        msg.message = message
        msg.save()
    except Exception as e:
        print(e)
        raise ClientError("MESSAGE_NOT_CREATE")
    return msg
