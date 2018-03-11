from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.widgets import TextInput, PasswordInput, EmailInput, FileInput
from accounts.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Login')
        }),
        label=_('Login'),
        error_messages={
            'invalid': _('Please enter a valid login'),
        }
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password')
        }),
        label=_('Password'),
    )

    def clean_username(self):
        try:
            username = self.cleaned_data['username']
        except KeyError:
            raise forms.ValidationError(_('Please enter a login'))

        existing = User.objects.filter(username__iexact=username)
        if not existing.exists():
            raise forms.ValidationError(_('User does not exist'))
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        try:
            user = authenticate(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
        except KeyError:
            raise forms.ValidationError(_('Incorrect password'))

        if user is None:
            raise forms.ValidationError(_('Incorrect password'))
        elif user is not None and not user.is_active:
            raise forms.ValidationError(_('Your account is inactive'))
        else:
            return self.cleaned_data['password']


class UserAddForm(forms.Form):
    username = forms.CharField(
        widget=TextInput(attrs={
            'id': 'username',
            'class': 'form-control',
            'placeholder': _('Enter your username')
        }),
        label=_('User name'),
    )
    email = forms.CharField(
        widget=EmailInput(attrs={
            'id': 'email',
            'class': 'form-control',
            'placeholder': _('Enter your email')
        }),
        label=_('Email'),
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'id': 'pass',
            'class': 'form-control',
            'autocomplete': 'off',
            'pattern': '.{8,}',
            'title': _('The password must contain more than 8 characters'),
            'placeholder': _('Enter your password')
        }),
        label=_('Password'),
    )
    password2 = forms.CharField(
        widget=PasswordInput(attrs={
            'id': 'pass2',
            'class': 'form-control',
            'autocomplete': 'off',
            'pattern': '.{8,}',
            'title': _('The password must contain more than 8 characters'),
            'placeholder': _('Enter your password')
        }),
        label=_('Repeat password'),
    )

    def clean_username(self):
        try:
            username = self.cleaned_data["username"]
        except KeyError:
            raise forms.ValidationError(_('You did not fill the field "User name"!'))
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with the username %s already registered!") % username)

    def clean_email(self):
        try:
            email = self.cleaned_data['email']
        except KeyError:
            raise forms.ValidationError(_('You did not fill the field "Email"!'))
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("A user with the email %s already registered!") % email)

    def clean_password(self):
        try:
            password = self.cleaned_data['password']
        except KeyError:
            raise forms.ValidationError(_('Enter password'))
        return password

    def clean_password2(self):
        try:
            password2 = self.cleaned_data['password2']
        except KeyError:
            raise forms.ValidationError(_('Enter repeat password'))
        try:
            password = self.cleaned_data['password']
        except KeyError:
            raise forms.ValidationError(_('Enter password'))
        if password != password2:
            raise forms.ValidationError(_('Passwords do not match'))
        else:
            return password2


class UserEditForm(forms.Form):
    id = forms.CharField(
        required=True,
        widget=TextInput(attrs={
            'id': 'id_user',
            'type': 'hidden'
        }),
    )
    username = forms.CharField(
        widget=TextInput(attrs={
            'id': 'username',
            'class': 'form-control',
            'placeholder': _('Enter your username')
        }),
        label=_('User name'),
        required=False,
    )
    surname = forms.CharField(
        widget=TextInput(attrs={
            'id': 'surname',
            'class': 'form-control',
            'placeholder': _('Enter your surname')
        }),
        label=_('User surname'),
        required=False,
    )
    nickname = forms.CharField(
        widget=TextInput(attrs={
            'id': 'nickname',
            'class': 'form-control',
            'placeholder': _('Enter your nickname')
        }),
        label=_('User nickname'),
        required=False,
    )
    email = forms.CharField(
        widget=EmailInput(attrs={
            'id': 'email',
            'class': 'form-control',
            'placeholder': _('Enter your email')
        }),
        label=_('Email'),
        required=False,
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'id': 'pass',
            'class': 'form-control',
            'autocomplete': 'off',
            'pattern': '.{8,}',
            'title': _('The password must contain more than 8 characters'),
            'placeholder': _('Enter your password')
        }),
        label=_('Password'),
        required=False,
    )
    password2 = forms.CharField(
        widget=PasswordInput(attrs={
            'id': 'pass2',
            'class': 'form-control',
            'autocomplete': 'off',
            'pattern': '.{8,}',
            'title': _('The password must contain more than 8 characters'),
            'placeholder': _('Enter your password')
        }),
        label=_('Repeat password'),
        required=False,
    )

    def clean_username(self):
        user_id = self.cleaned_data["id"]
        try:
            username = self.cleaned_data["username"]
        except KeyError:
            raise forms.ValidationError(_('You did not fill the field "User name"!'))
        try:
            user = User.objects.get(id=user_id)
            if user.username == username:
                return username
        except User.DoesNotExist:
            raise forms.ValidationError(_('You did not fill the field "User name"!'))
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with the username %s already registered!") % username)

    def clean_email(self):
        user_id = self.cleaned_data["id"]
        try:
            email = self.cleaned_data['email']
        except KeyError:
            raise forms.ValidationError(_('You did not fill the field "Email"!'))
        try:
            user = User.objects.get(id=user_id)
            if user.email == email:
                return email
        except User.DoesNotExist:
            raise forms.ValidationError(_('You did not fill the field "Email"!'))
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("A user with the email %s already registered!") % email)

    def clean_password(self):
        try:
            password = self.cleaned_data['password']
        except KeyError:
            raise forms.ValidationError(_('Enter password'))
        return password

    def clean_password2(self):
        try:
            password2 = self.cleaned_data['password2']
        except KeyError:
            raise forms.ValidationError(_('Enter repeat password'))
        try:
            password = self.cleaned_data['password']
        except KeyError:
            raise forms.ValidationError(_('Enter password'))
        if password != password2:
            raise forms.ValidationError(_('Passwords do not match'))
        else:
            return password2
