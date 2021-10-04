from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, name, birth, started_working, team, password=None):
        if not username:
            raise ValueError('must have user username')
        if not name:
            raise ValueError('must have user name')
        if not birth:
            raise ValueError('must have user birth')
        if not started_working:
            raise ValueError('must have user started_working')
        if not team:
            raise ValueError('must have user team')
        user = self.model(
            username=username,
            name=name,
            birth=birth,
            started_working=started_working,
            team=team,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, birth, started_working, team, password):
        user = self.create_user(
            username=username,
            name=name,
            birth=birth,
            started_working=started_working,
            team=team,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=100,unique=True,)
    name = models.CharField(max_length=10,unique=True,)
    birth = models.DateField()
    started_working = models.DateField()
    team = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'birth','started_working','team']
    
    def __str__(self):
        return self.username
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin