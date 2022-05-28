from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=2000)
    body = models.CharField(max_length=2000)

    def __str__(self):
        return self.title