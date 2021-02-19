from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser

class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> DiscordUser:
        findUser = DiscordUser.objects.filter(id=user['id'])
        if len(findUser) == 0:
            newUser = DiscordUser.objects.createNewUser(user)
            return newUser
        return findUser

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None 