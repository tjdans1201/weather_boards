from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "author", "title", "updated_at"]


class BoardDetailSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["author", "title", "content", "current_weather", "updated_at"]
