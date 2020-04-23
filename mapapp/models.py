from django.db import models

# Create your models here.
class Courses(models.Model):
    name = models.CharField(max_length=100)
    pneumonic = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class MeetingArea(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    def __str__(self):
        return self.name

