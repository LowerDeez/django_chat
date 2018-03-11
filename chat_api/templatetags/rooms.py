from django import template
register = template.Library()


@register.filter(name='room_avatar')
def get_room_avatar(members, user):
    if members.count() >= 2:
        img = ''
        for u in members:
            if u != user:
                img = u.avatar.url
                break
        return img
    else:
        return members.first().avatar.url


@register.filter(name='room_title')
def get_room_title(members, user):
    if members.count() >= 2:
        username = ''
        for u in members:
            if u != user:
                username = u.username
                break
        return username
    else:
        return members.first().username
