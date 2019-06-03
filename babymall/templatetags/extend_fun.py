from django import template
from ..models import *

register = template.Library()
# 自定义标签
@register.simple_tag
def getshopcart(user):
    users = MyUser.objects.get(username=user.username)
    return Shop.objects.filter(user_id=users).count()

@register.simple_tag
def getsuer(user):
    users = MyUser.objects.get(username=user.username)
    return users.id

@register.simple_tag
def getcomid(aid):
    cls = Classify.objects.get(pk=aid)
    return cls