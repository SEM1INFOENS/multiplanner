from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_transaction(tr):
    name = tr.__str__()
    url = tr.get_absolute_url()
    str = "<a href=\"{}\">{}</a>".format(url, name)
    return mark_safe(str)
