from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.EmailField(unique=True)

    # 인적 사항: 이름, 나이, 사진
    name = models.CharField(max_length=100)
    age = models.DateField()
    photo = models.ImageField(upload_to='images/', blank=True)

    # 인사 정보: 사원 번호, 입사 연도, 직급, 소속팀
    emp_id = models.CharField(max_length=100, unique=True)
    emp_date = models.DateField()
    emp_grade = models.CharField(max_length=10)
    emp_team = models.CharField(max_length=10)

    REQUIRED_FIELDS = ['name', 'age', 'emp_id', 'emp_date', 'emp_grade', 'emp_team']

    def __str__(self):
        return f'{self.name} 사원'  # "박상현 사원"
