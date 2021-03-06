from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_delete, pre_save

from puplic_profile.models import ProfileUser
#####################################Craete custom User#####################################
class BasicInfoManager(BaseUserManager):

  def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
    if not email:
      raise ValueError('User shold be have an email')

    if not password:
      raise ValueError('User should be have a password')
    user = self.model(
      email = self.normalize_email(email),
    )
    user.active = is_active
    user.staff  = is_staff
    user.admin  = is_admin
    user.set_password(password)
    user.save(using= self._db)

    return user

  def create_staffuser(self, email, password=None,):
    user = self.create_user(
      email,
      password= password,
      is_staff = True
    )

    return user

  def create_superuser(self, email, password=None):
    user = self.create_user(
      email,
      password= password,
      is_staff= True,
      is_admin= True
    )

    return user


class User(AbstractBaseUser):
  email         = models.EmailField(max_length=150, unique=True)
  password      = models.CharField(max_length=15)
  active        = models.BooleanField(default=True)
  staff         = models.BooleanField(default= False)
  admin         = models.BooleanField(default= False)

  objects       = BasicInfoManager()

  USERNAME_FIELD  = 'email'
  REQUIRED_FIELDS = []

  class Meta:
    verbose_name         = 'User'
    verbose_name_plural  = 'Users'

  def __str__(self):
      return self.email
  
  def get_full_name(self):
    return self.email

  def get_short_name(self):
    return self.email

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True


  @property
  def is_staff(self):
    return self.staff
  @property
  def is_admin(self):
    return self.admin
