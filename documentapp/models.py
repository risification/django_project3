from django.db import models


# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    file = models.FileField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_expired = models.DateField()
    status = models.CharField(choices=(
        ('active', 'active'),
        ('dead', 'dead')
    ), max_length=30)
    document_root = models.CharField(choices=(
        ('public', 'public'),
        ('private', 'private'),
        ('secret', 'secret'),
        ('top-secret', 'top-secret')
    ), max_length=30)
