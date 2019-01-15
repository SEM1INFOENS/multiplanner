from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_user(user):
    from permissions.templatetags.permissions_filters import is_app_admin
    username = user.username
    user_url = reverse('users:page', args=(username,))
    if is_app_admin(user):
        admin_logo = "<i class=\"fas fa-shield-alt\"></i>"
    else:
        admin_logo = ""
    str = "<a href=\"{}\">{}{}</a>".format(user_url, username, admin_logo)
    return mark_safe(str)
