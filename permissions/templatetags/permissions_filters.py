from django import template

register = template.Library()

@register.filter
def is_app_admin(user):
    from permissions.group import admins
    return admins() in user.groups.all()
