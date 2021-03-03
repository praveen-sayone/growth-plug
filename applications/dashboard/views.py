import facebook
import requests

# Create your views here.
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.fb_handler import FaceBookPageHandler
from applications.dashboard.models import FacebookToken
from applications.dashboard.serializers import FacebookTokenSerializer, AboutPageSerializer


class LoginPageView(TemplateView):
    template_name = 'index.html'


class SocialUserLoginAPI(APIView):

    def post(self, request):
        serializer = FacebookTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                graph = facebook.GraphAPI(access_token=serializer.validated_data['access_token'])
                user_details = graph.get_object(id='me', fields='first_name, last_name, email')
                if User.objects.filter(username__iexact=user_details.get('id')).exists():
                    user = User.objects.get(username__iexact=user_details.get('id'))
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'message': 'success', 'key': token.key})
                else:
                    data = {'username': user_details.get('id'),
                            'password': User.objects.make_random_password(),
                            'first_name': user_details.get('first_name'),
                            'last_name': user_details.get('last_name'),
                            'is_active': True}
                    user = User.objects.create(**data)
                    token, created = Token.objects.get_or_create(user=user)
                    token_str = serializer.validated_data['access_token']
                    user_token = FaceBookPageHandler.extended_user_token(token_str)['access_token']
                    url = 'https://graph.facebook.com/{}/accounts?fields=name,access_token&access_token={}'.format(user_details['id'], token_str)
                    response = requests.get(url)
                    result = response.json()
                    if response.status_code == 200 and len(result['data']):
                        social_token = {'type': 'facebook', 'page_id': result['data'][0]['id'], 'user': user, 'user_token': user_token}
                        FacebookToken.objects.create(**social_token)

                    return Response({'message': 'success', 'key': token.key})
            except Exception as e:
                return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class SocialMediaPages(TemplateView):
    template_name = 'social-media-pages.html'

    def get_context_data(self, **kwargs):
        token = str(self.request.headers['Cookie']).split("Token ")[1]
        return {'user': Token.objects.get(key=token).user}


class FetchAboutPage(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.fb_tokens.exists():
            facebook_client = FaceBookPageHandler(request.user)
            result = facebook_client.get_page_info()
            return Response({'message': [result.json()]}, status=200)
        return Response({'message': "No pages"}, status=status.HTTP_403_FORBIDDEN)


class UpdateAboutPage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AboutPageSerializer(data=request.data)
        if serializer.is_valid() and request.user.fb_tokens.exists():
            facebook_client = FaceBookPageHandler(request.user)
            response = facebook_client.update_page_info(serializer.validated_data)
            if response.status_code == 200:
                return Response({'message': response.json()})
            else:
                return Response(response.json()['error'], status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


