'''Models for the relationships app'''

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Friendships(models.Model):
    '''Friendships is an extension for Users which adds a list of friends and a list of invited
    friends. It is symmetrical.'''
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(User, related_name='+')
    invited_list = models.ManyToManyField(User, related_name='+')

    def __repr__(self):
        '''Enables to display a Friendships object in a convenient way'''
        return "user : {}, friend_list : {}, invited_list : {}".format(self.user,
            self.friend_list, self.invited_list)


MARK_MIN = -10
MARK_MAX = 10

class SecretMark(models.Model):
    '''Users can mark other users.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marked_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    mark = models.IntegerField(validators=
                               [MaxValueValidator(MARK_MIN),
                                MinValueValidator(MARK_MAX)])


    def __repr__(self):
        '''Enables to display a SecretMark in a convenient way'''
        return "user : {}, marked_user : {}, mark : {}".format(self.user,
            self.marked_user, self.mark)

