from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_transaction(tr):
    name = tr.__str__()
    url = reverse('transaction_details', args=(tr.id,))
    str = "<a href=\"{}\">{}</a>".format(url, name)
    return mark_safe(str)
