from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import MinValueValidator, RegexValidator


class WarehouseUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, date_of_birth, email, gender,
                    phone_number=None, password=None, is_active=True,
                    is_admin=False, is_staff=False, employee_id=None):

        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must provide password")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          date_of_birth=date_of_birth,
                          gender=gender,
                          phone_number=phone_number,
                          employee_id=employee_id)
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name, last_name, date_of_birth, email,
                         gender, phone_number, employee_id, password):
        user = self.create_user(first_name=first_name,
                                last_name=last_name,
                                date_of_birth=date_of_birth,
                                gender=gender,
                                phone_number=phone_number,
                                employee_id=employee_id,
                                email=email,
                                password=password,
                                is_staff=True)
        return user

    def create_superuser(self, first_name, last_name, date_of_birth, email,
                         gender, phone_number, employee_id, password):
        user = self.create_user(first_name=first_name,
                                last_name=last_name,
                                date_of_birth=date_of_birth,
                                gender=gender,
                                phone_number=phone_number,
                                employee_id=employee_id,
                                password=password,
                                email=email,
                                is_staff=True,
                                is_admin=True)
        return user


class WarehouseUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(default='1993-01-01')
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    gender = models.CharField(max_length=6, blank=False, default='Male', choices=GENDER_CHOICES)
    phone_regex = RegexValidator(r'^\+?[0-9]{1,2}?\s?[0-9]{10}$',
                                 message="Phone number must be in format: country code and number(ex +1 123456790")
    phone_number = models.CharField(validators=[phone_regex],max_length=14, blank=True, null=True)
    employee_id = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    objects = WarehouseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'gender',
                       'phone_number', 'employee_id']

    def __str__(self):
        return self.email

    def get_username(self):
        if self.email:
            return self.email

    def has_perm(self, perm, obj=None):
        """Check whether user has specific permission"""
        if not self.staff:
            return False
        return True

    def has_module_perms(self, app_label):
        """Check whether has permission to view the app"""
        if not self.staff:
            return False
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a member of staff"""
        return self.admin
