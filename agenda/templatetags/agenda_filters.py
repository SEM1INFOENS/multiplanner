from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_event_logo(obj):
    name = obj.__str__()
    url = obj.get_absolute_url()
    if not obj.is_over():
        pref = "<i class=\"far fa-calendar-alt\"></i> "
    else:
        pref = "<i class=\"far fa-calendar-times\"></i> "    
    str = "<a href=\"{}\">{}{}</a>".format(url, pref, name)
    return mark_safe(str)

@register.filter
def display_event(obj):
    name = obj.__str__()
    url = obj.get_absolute_url()
    str = "<a href=\"{}\">{}</a>".format(url, name)
    return mark_safe(str)
