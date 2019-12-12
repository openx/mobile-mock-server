from django.db import models


# Create your models here.
class LogModel(models.Model):
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    path = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    body = models.TextField()
    query_string = models.TextField()