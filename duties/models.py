from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Nurse(models.Model):
    nurse = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    off_choices = models.JSONField()
    duties = models.JSONField()


class Team(models.Model):
    pass
