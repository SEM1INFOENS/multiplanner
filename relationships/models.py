from django.db import models


class Friendships(models.Model):
    '''Friendships is an extension for Users which adds a list of friends and a list of invited
    friends. It is symmetrical.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(User)
    invited_list = models.ManyToManyField(User)

mark_min=-10
mark_max= 10
class SecretMark(models.Model):
    '''Users can mark other users'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marked_user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(validators=
                               [MaxValueValidator(mark_min),
                                MinValueValidator(mark_max)])
