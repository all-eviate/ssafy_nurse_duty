from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """
    3 types(★: 필수항목)

    1. technical info
        user_id: 이메일 ★ / (rowid, password) (1)

    2. personal info
        name: 이름 ★, age: 생년월일(datetype) ★, photo: 증명사진, address: 주소 (4)
    
    3. social info (regarding working environment)
        emp_id: 사원번호 ★, emp_date: 입사일(datetype) ★, emp_team: 소속팀 ★, emp_grade: 직급 ★ (4)
    """
    def create_user(self, user_id, name, age, photo, address, emp_id, emp_date, emp_team, emp_grade, password=None):
        # 나중에 에러 메시지 수정해야 합니다.
        if not user_id:
            raise ValueError('User ID로 이메일을 입력하세요. 사원번호가 아닙니다. 알겠습니까?')
        if not name:
            raise ValueError('너의 이름은?')
        if not age:
            raise ValueError('나이를 부끄러워 하지마! 넌 젊어!')
        if not emp_id:
            raise ValueError('필수 항목입니다! 사원번호를 입력해주세요 :)')
        if not emp_date:
            raise ValueError('마! 짬밥 좀 되나?')
        if not emp_team:
            raise ValueError('너 사수 데려와')
        if not emp_grade:
            raise ValueError('필수 항목입니다! 직급을 선택해주세요 :)')

        user = self.model(
            user_id=user_id,
            name=name,
            age=age,
            photo=photo,
            address=address,
            emp_id=emp_id,
            emp_date=emp_date,
            emp_team=emp_team,
            emp_grade=emp_grade,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, age, photo, address, emp_id, emp_date, emp_team, emp_grade, password):
        user = self.create_user(
            user_id=user_id,
            password=password,
            name=name,
            age=age,
            photo=photo,
            address=address,
            emp_id=emp_id,
            emp_date=emp_date,
            emp_team=emp_team,
            emp_grade=emp_grade,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    age = models.DateField()
    photo = models.ImageField(upload_to='user_info_photos/', blank=True)
    address = models.CharField(max_length=100, blank=True)
    emp_id = models.CharField(max_length=10, unique=True)
    emp_date = models.DateField()
    emp_team = models.IntegerField()
    emp_grade = models.CharField(max_length=10)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'age', 'photo', 'address', 'emp_id', 'emp_date', 'emp_team', 'emp_grade']
    
    def __str__(self):
        return self.name
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
