from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Nurse(models.Model):
    """
    3 Fields(★: 필수항목)

    * user: User Model과 1대1로 연결된 외래키(FK) 필드 ★
    * choices: 간호사가 선택한 off days ★
    * duties: 알고리즘의 결과값으로서 개인별 가능한 듀티들이 담길 필드
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    choices = models.JSONField()
    duties = models.JSONField(blank=True, null=True)


class Team(models.Model):
    """
    2 Fields(★: 필수항목)

    * team: 팀 번호 ★
    * duty: 알고리즘의 결과값으로서 팀별 듀티가 담길 필드 ★
    """
    team=models.IntegerField()
    duty=models.JSONField()
