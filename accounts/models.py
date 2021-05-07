from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Dossier(models.Model):
    full_name = models.CharField(max_length=50)
    date_birth = models.DateField()
    image = models.ImageField(blank=True, null=True)
    gender_type = (
        ("M", "M"),
        ("F", "F")
    )
    gender = models.CharField(choices=gender_type, max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Car(models.Model):
    mark = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.DateField()
    number = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=50)
    type = models.CharField(choices=(
        ('mazda', 'mazda'),
        ('mers', 'mers')
    ), max_length=30)
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='car')


class Education(models.Model):
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    school_name = models.CharField(max_length=30)
    major = models.CharField(max_length=30)
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='education')


class Warcraft(models.Model):
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    military_area = models.CharField(max_length=30)
    major = models.CharField(max_length=30)
    start_pose = models.DateField(auto_now_add=True)
    end_pose = models.DateField()
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='warcraft')
