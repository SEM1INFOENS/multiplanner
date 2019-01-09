from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_group_logo(obj):
    name = obj.__str__()
    url = obj.get_absolute_url()
    str = "<a href=\"{}\"><i class=\"fas fa-users\"></i> {}</a>".format(url, name)
    return mark_safe(str)

@register.filter
def display_group(obj):
    name = obj.__str__()
    url = obj.get_absolute_url()
    str = "<a href=\"{}\">{}</a>".format(url, name)
    return mark_safe(str)
