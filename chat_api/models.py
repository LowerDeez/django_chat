from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from accounts.models import User
from django_resized import ResizedImageField


class Room(models.Model):
    TYPE_CHOICES = (
        (1, 'person'),
        (2, 'group'),
    )

    title = models.CharField(max_length=255, null=True, default=None)
    avatar = ResizedImageField(size=[50, 50], quality=75, max_length=256,
                               default='chats/default/avatar.png', verbose_name=_('avatar'))
    avatar_big = ResizedImageField(size=[150, 150], quality=75, max_length=256,
                                   default='chats/default/avatar_150x150.png', verbose_name=_('avatar'))
    chat_type = models.IntegerField(verbose_name=_('Chat type'), default=1, choices=TYPE_CHOICES, db_index=True)
    label = models.SlugField(blank=True, null=True)
    members = models.ManyToManyField(User)
    last_time = models.DateTimeField(default=timezone.now, db_index=True)

    @property
    def formatted_last_time(self):
        return self.last_time.timestamp()

    def __str__(self):
        return str(self.id)

    @property
    def group_name(self):
        return "room-%s" % self.id

    def last_message(self):
        msg = Message.objects.filter(room_id=self.id).last()
        if msg:
            return str(msg.message)
        else:
            return ''

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    type = models.CharField(verbose_name=_('Type of message'), max_length=64, blank=True, default='default')
    type_href = models.IntegerField(verbose_name=_('Id references'), blank=True, null=True)

    @property
    def formatted_timestamp(self):
        return self.timestamp.timestamp()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
