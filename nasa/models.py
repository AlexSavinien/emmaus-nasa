from django.db import models

# Create your models here.


class Asteroid(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    distance = models.CharField(max_length=200)
    dateClosest = models.DateTimeField()
    previousApproaches = []
    nextApproaches = []
    firstObservationDate = models.DateTimeField()
    lastObservationDate = models.DateTimeField()
    nextObservation = models.DateTimeField()
    dataArcInDays = models.CharField(max_length=200)
    nextObservation = models.DateTimeField()

    def __str__(self):
        return str(self.name)


class Approach(models.Model):
    asteroidId = models.CharField(max_length=50, primary_key=True)
    approachDate = models.DateTimeField()
    distance = models.CharField(max_length=200)

    def __str__(self):
        return str(self.approachDate)
