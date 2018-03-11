from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField

AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = True
AbstractUser._meta.get_field('email').null = True


class User(AbstractUser):
    surname = models.CharField(verbose_name=_('Surname'), max_length=128, blank=True)
    nickname = models.CharField(verbose_name=_('Nickname'), max_length=128, blank=True)
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    avatar = ResizedImageField(size=[50, 50], quality=75, max_length=256,
                               default='accounts/default/avatar.png', verbose_name=_('avatar'))
    avatar_big = ResizedImageField(size=[150, 150], quality=75, max_length=256,
                                   default='accounts/default/avatar_150x150.png', verbose_name=_('avatar'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
