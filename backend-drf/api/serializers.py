from rest_framework import serializers


class NepsePredictionSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length = 20)