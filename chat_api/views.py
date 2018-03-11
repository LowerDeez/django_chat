from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.urls import reverse
from chat_api.models import Room, Message
from chat_api.forms import RoomUserAddForm, RoomChatAddForm
from accounts.models import User
from optimize_image.utils import OptimizeImage
from uuid import uuid4
import base64
import os


def make_response(status=200, content_type='application/json', content=None):
    response = HttpResponse()
    response.status_code = status
    response['Content-Type'] = content_type
    response.content = content
    return response


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        user = request.user
        if user is not None and user.is_active:
            rooms = Room.objects.prefetch_related('messages')\
                .filter(members__id=user.id).order_by('-last_time')

            context = {
                'user': user,
                'rooms': rooms,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("login"))


class ChatRoomsView(View):
    template_name = 'chat_rooms.html'

    def get(self, request, pk):
        user = request.user
        if user is not None and user.is_active:
            rooms = Room.objects.prefetch_related('messages')\
                .filter(members__id=user.id).order_by('-last_time')

            context = {
                'rooms': rooms,
                'room_active': int(pk),
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("login"))


class ChatRoomMessagesView(View):
    template_name = 'get_messages.html'

    def get(self, request, pk):
        user = request.user
        if user is not None and user.is_active:
            room = Room.objects.get(id=pk)
            messages = Message.objects.filter(room_id=pk)

            context = {
                'user': user,
                'room': room,
                'messages': messages,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("login"))


class NewChatView(View):
    form_class = RoomUserAddForm
    initial = {}
    template_name = 'add_user_room.html'

    form_class_two = RoomChatAddForm
    initial_two = {}
    template_name_two = 'add_chat_room.html'

    def get(self, request, room_type):
        user = request.user
        if user is not None and user.is_active:
            if int(room_type) == 1:
                form = self.form_class(initial=self.initial)
                context = {
                    'user': user,
                    'form': form,
                }
                return render(request, self.template_name, context)
            else:
                form_two = self.form_class_two(initial=self.initial_two)
                context = {
                    'user': user,
                    'form': form_two,
                }
                return render(request, self.template_name_two, context)
        else:
            return HttpResponseRedirect(reverse("login"))

    def post(self, request, room_type, *args, **kwargs):
        if int(room_type) == 1:
            form = self.form_class(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.POST['username'])
                return add_new_user_room(
                    request,
                    request.user,
                    user
                )
            return render(request, self.template_name, {'form': form})
        else:
            form_two = self.form_class_two(request.POST)
            if form_two.is_valid():
                users_list = str(request.POST['users_list']).split(',')[:-1]
                title = str(request.POST['title'])
                image_64 = str(request.POST['image_64'])

                return add_new_chat_room(
                    request,
                    request.user,
                    users_list,
                    title,
                    image_64
                )
            return render(request, self.template_name_two, {'form': form_two})


def add_new_user_room(request, m_user, user):
    try:
        room = Room()
        room.chat_type = 1
        room.save()
        room.members.add(m_user)
        room.members.add(user)
        m_user.friends.add(user)
        room.save()
        return HttpResponseRedirect(reverse("main"))
    except Exception as e:
        raise e


def add_new_chat_room(request, m_user, users_list, title, image_64):
    try:
        image_type = str(str(image_64).split(',')[0].split('/')[1].split(';')[0])
        image_64_encode = str(image_64).split(',')[1]
        file_name = str(uuid4()) + '.' + image_type
        base_dir = os.path.dirname(os.path.dirname(__file__))
        avatar_name = str(base_dir) + '/media/chats/' + file_name
        image_64_decode = base64.b64decode(image_64_encode)
        image_result = open(avatar_name, 'wb')
        image_result.write(image_64_decode)
        image_result.close()
        o_image = OptimizeImage(open(avatar_name, "rb"), 'chats')
        image_data = o_image.optimize_image()
        os.remove(avatar_name)
        room = Room()
        room.chat_type = 2
        room.title = title
        room.avatar = image_data.get('name')
        room.avatar_big = image_data.get('name_big')
        room.save()
        room.members.add(m_user)
        for u in users_list:
            room.members.add(u)
        room.save()
        return HttpResponseRedirect(reverse("main"))
    except Exception as e:
        raise e
