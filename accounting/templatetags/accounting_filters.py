from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_transaction(tr):
    name = tr.__str__()
<<<<<<< HEAD
    url = tr.get_absolute_url()
=======
    url = reverse('transaction_details', args=(tr.id,))
>>>>>>> cf4b60ff255150906e506af9919692c6cfc0d5dd
    str = "<a href=\"{}\">{}</a>".format(url, name)
    return mark_safe(str)
