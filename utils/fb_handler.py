import urllib

import requests
from django.conf import settings


class FaceBookPageHandler(object):

    BASE_URL = 'https://graph.facebook.com/v8.0'

    def __init__(self, user):
        fb_token = user.fb_tokens.first()
        self.ACCESS_TOKEN = fb_token.user_token
        self.PAGE_ID = fb_token.page_id
        self.PAGE_ACCESS_TOKEN = self.extended_page_token(self.PAGE_ID, self.ACCESS_TOKEN)

    def get_page_info(self):
        url = '{}/{}?fields=name,phone,about,emails,website&access_token={}'.format(self.BASE_URL, self.PAGE_ID, self.ACCESS_TOKEN)
        result = requests.get(url)
        return result

    def update_page_info(self, data):
        encoded_data = urllib.parse.urlencode(data)
        url = '{}/{}?{}&access_token={}'.format(self.BASE_URL, self.PAGE_ID, encoded_data, self.PAGE_ACCESS_TOKEN)
        result = requests.post(url)
        return result

    @staticmethod
    def extended_user_token(short_lived_user_token):
        url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}' \
              '&client_secret={}&fb_exchange_token={}'.format(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET, short_lived_user_token)
        response = requests.get(url)
        return response.json()

    @staticmethod
    def extended_page_token(page_id, user_token):
        url = 'https://graph.facebook.com/{}?fields=access_token&access_token={}'.format(page_id, user_token)
        response = requests.get(url)
        return response.json()['access_token']
