from django.db import models
from tinymce.models import HTMLField


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256, default='')
    body = HTMLField()
    owner = models.ForeignKey('auth.User', related_name='articles', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

