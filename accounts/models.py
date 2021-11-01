from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 서비스 ID
    username = models.EmailField(unique=True)

    # 기본 인적 사항(이름, 나이, 사진)
    name = models.CharField(max_length=100)
    age = models.DateField()
    photo = models.ImageField(upload_to='images/', blank=True)

    # 인사 정보(사원 번호, 입사 연도, 직급, 소속팀)
    emp_id = models.CharField(max_length=100)
    emp_date = models.DateField()
    emp_grade = models.CharField(max_length=10)
    emp_team = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.pk}: {self.name}사원({self.emp_id})'
