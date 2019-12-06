from django.db import models

class Book(models.Model):

    location = models.CharField(max_length=60)
    no_of_students = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.location
