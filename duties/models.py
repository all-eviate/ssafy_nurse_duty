from django.db import models

class Team(models.Model):
    date = models.DateField()
    duty = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.date
