from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.widgets import TextInput, HiddenInput
from accounts.models import User


class RoomUserAddForm(forms.Form):
    username = forms.CharField(
        widget=TextInput(attrs={
            'id': 'username',
            'class': 'form-control',
            'placeholder': _('Enter username')
        }),
        label=_('User name'),
    )

    def clean_username(self):
        try:
            username = self.cleaned_data["username"]
        except KeyError:
            raise forms.ValidationError(_('You did not fill the field "User name"!'))
        try:
            User._default_manager.get(username=username)
            return username
        except User.DoesNotExist:
            raise forms.ValidationError(_("A user with the username %s does not exist!") % username)


class RoomChatAddForm(forms.Form):
    title = forms.CharField(
        widget=TextInput(attrs={
            'id': 'title',
            'class': 'form-control',
            'placeholder': _('Enter title')
        }),
        label=_('Title'),
    )
    image_64 = forms.CharField(
        widget=HiddenInput(attrs={
            'id': 'image_64'
        }),
        required=False,
    )
    users_list = forms.CharField(
        widget=HiddenInput(attrs={
            'id': 'users_list'
        }),
        required=False,
    )

    def clean_title(self):
        try:
            return self.cleaned_data["title"]
        except KeyError:
            raise forms.ValidationError(_('You did not fill the field "Title"!'))
