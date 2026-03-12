from django.db import models

# Create your models here.
class Election(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=255)
