from rest_framework import serializers


class FacebookTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(allow_blank=False, trim_whitespace=True)


class AboutPageSerializer(serializers.Serializer):
    about = serializers.CharField(required=False, allow_null=True, allow_blank=True)
