from django.db import models

# Create your models here.
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=200)
    current_wheater = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
