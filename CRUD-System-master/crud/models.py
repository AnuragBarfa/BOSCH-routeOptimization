from django.db import models

class Book(models.Model):
    location = models.CharField(max_length=60)
    timestamp = models.CharField(max_length=60)
    no_of_students = models.IntegerField()


    def __str__(self):
        return self.location
