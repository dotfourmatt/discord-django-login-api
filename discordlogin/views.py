from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views import generic

from .models import DiscordUser
from oauth2discord.settings import DiscordOAuth2
import requests

class indexView(generic.TemplateView):
    template_name = 'discordlogin/index.html'

class discordLoginView(generic.View):
    def get(self, request):
        # if the user is logged in, they will be redirected.
        if self.request.user.is_authenticated:
            return redirect("index")

        # If the 'QUERY_STRING' is > 0, that means the code is in the url ==> oauth2/login?code=********
        elif len(self.request.META['QUERY_STRING']) > 0:
            code = self.request.GET.get('code')
            getUser = self.exchangeCode(code)
            user = authenticate(request, user=getUser)
            user = list(user).pop()
            login(request, user)
            return redirect("index")

        # redirects to discord api
        else:
            return redirect(DiscordOAuth2["DISCORD_OAUTH2_URL"])

    # retrives user data from discord api
    def exchangeCode(self, code: str):
        data = {
            "client_id": DiscordOAuth2["CLIENT_ID"],
            "client_secret": DiscordOAuth2["CLIENT_SECRET"],
            'grant_type': 'authorization_code',
            "code": code,
            "redirect_uri": DiscordOAuth2["REDIRECT_URI"],
            "scope": "identify"
        }
        response = requests.post(f"{DiscordOAuth2['API_ENDPOINT']}/oauth2/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        response.raise_for_status()
        response = requests.get(f"{DiscordOAuth2['API_ENDPOINT']}/users/@me", headers={"Authorization": f"Bearer {response.json()['access_token']}"})
        return response.json()