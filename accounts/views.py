from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.urls import reverse
from django.contrib import auth, messages
from accounts.forms import LoginForm, UserAddForm, UserEditForm
from accounts.models import User
from optimize_image.utils import OptimizeImage
from uuid import uuid4
import base64
import json
import os


class LoginView(View):
    form_class = LoginForm
    initial = {}
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return login(
                request,
                request.POST['username'],
                request.POST['password']
            )

        return render(request, self.template_name, {'form': form})


def login(request, username, password):
    user = auth.authenticate(
        username=username,
        password=password
    )

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(reverse("main"))
    else:
        return redirect_with_message(
            request,
            messages.ERROR,
            _('Please enter a valid login'),
            "login"
        )


def redirect_with_message(request, message_type, message_text, redirect_page):
    messages.add_message(
        request,
        message_type,
        message_text
    )
    return HttpResponseRedirect(reverse(redirect_page))


class RegisterView(View):
    form_class = UserAddForm
    initial = {}
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return register(
                request,
                request.POST['username'],
                request.POST['password'],
                request.POST['email']
            )
        return render(request, self.template_name, {'form': form})


def register(request, username, password, email):
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except Exception as e:
        raise e

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(reverse("main"))
    else:
        return HttpResponseRedirect(reverse("login"))


class UserView(View):
    template_name = 'user_view.html'

    def get(self, request, pk):
        user = request.user
        if user is not None and user.is_active:
            m_user = User.objects.get(id=pk)
            context = {
                'm_user': m_user,
                'user': user
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("login"))


class UserEditView(View):
    form_class = UserEditForm
    initial = {}
    template_name = 'user_edit.html'

    def get(self, request, pk):
        user = request.user
        if user is not None and user.is_active:
            self.initial = {
                'id': pk,
                'username': user.username,
                'surname': user.surname,
                'nickname': user.nickname,
                'email': user.email,
            }
            form = self.form_class(initial=self.initial)
            m_user = User.objects.get(id=pk)
            context = {
                'form': form,
                'm_user': m_user
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("login"))

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return user_update(
                request,
                request.POST['username'],
                request.POST['email'],
                request.POST['surname'],
                request.POST['nickname'],
                request.POST['password']
            )
        return render(request, self.template_name, {'form': form})


def user_update(request, username, email, surname=None, nickname=None, password=None):
    try:
        user = User.objects.get(username=username)
        user.username = username
        user.email = email
        if surname != '' and surname is not None:
            user.surname = surname
        if nickname != '' and nickname is not None:
            user.nickname = nickname
        if password != '' and password is not None:
            user.set_password(password)
        user.save()
        return HttpResponseRedirect(reverse("user_view", kwargs={'pk': user.id}))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("main"))
    else:
        return HttpResponseRedirect(reverse("login"))


def save_photo_user(request, pk):
    if request.method == 'POST':
        user = request.user
        if user is not None and user.is_active:
            try:
                m_user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return HttpResponse(json.dumps({'result': 'false'}), content_type="application/json")

            user_avatar = request.POST.get('image', None)
            if user_avatar is not None and user_avatar != '':
                image_type = str(str(user_avatar).split(',')[0].split('/')[1].split(';')[0])
                image_64_encode = str(user_avatar).split(',')[1]
                file_name = str(uuid4()) + '.' + image_type
                base_dir = os.path.dirname(os.path.dirname(__file__))
                avatar_name = str(base_dir) + '/media/accounts/' + file_name
                image_64_decode = base64.b64decode(image_64_encode)
                image_result = open(avatar_name, 'wb')
                image_result.write(image_64_decode)
                image_result.close()
                o_image = OptimizeImage(open(avatar_name, "rb"), 'accounts')
                image_data = o_image.optimize_image()
                m_user.avatar = image_data.get('name')
                m_user.avatar_big = image_data.get('name_big')
                m_user.save()
                os.remove(avatar_name)
                data = json.dumps({
                    'result': 'true',
                    'image_big': str(m_user.avatar_big)
                })
                return HttpResponse(data, content_type="application/json")
            else:
                return HttpResponse(json.dumps({'result': 'false'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'result': 'false'}), content_type="application/json")


def delete_photo_user(request, pk):
    if request.method == 'POST':
        user = request.user
        if user is not None and user.is_active:
            try:
                m_user = User.objects.get(id=pk)
                m_user.avatar = 'accounts/default/avatar.png'
                m_user.avatar_big = 'accounts/default/avatar_150x150.png'
                m_user.save()
                data = json.dumps({
                    'result': 'true',
                    'image_big': str(m_user.avatar_big)
                })
                return HttpResponse(data, content_type="application/json")
            except User.DoesNotExist:
                return HttpResponse(json.dumps({'result': 'false'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'result': 'false'}), content_type="application/json")
