from django.contrib.auth.models import User
from django.db import models


class FacebookToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fb_tokens')
    type = models.CharField(max_length=100)
    user_token = models.TextField(max_length=250, null=True, blank=True)
    page_id = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.type
