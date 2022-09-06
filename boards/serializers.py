from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title", "content","author", "created_at","current_weather","updated_at"]

class BoardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id","author", "title", "content", "current_weather","created_at","updated_at"]

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["author", "title", "content", "current_weather", "password"]

class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title","content","updated_at"]

