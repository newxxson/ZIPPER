from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from zip.models import Area, House, Review
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, id, nickname, password=None, **extra_fields):
        if not email:
            print(email, id, nickname, password, extra_fields)
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        interested_areas = extra_fields.pop("interested_areas", [""])
        user = self.model(email=email, id=id, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        interested_areas = Area.objects.filter(pk__in=interested_areas)
        user.interested_areas.set(interested_areas)
        return user

    def create_superuser(self, email, id, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        print(extra_fields)
        return self.create_user(email, id, nickname, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        verbose_name="ID", max_length=50, unique=True, primary_key=True
    )
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name="Nickname",
        max_length=50,
        unique=True,
    )

    student_number = models.PositiveIntegerField(null=True)

    sex_choices = [("M", "Male"), ("F", "Female"), ("NM", "Not to mention")]
    sex = models.CharField(
        max_length=2,
        choices=sex_choices,
        default="NM",
    )

    department = models.CharField(max_length=50, null=True, blank=True)

    interested_areas = models.ManyToManyField(
        Area, related_name="interested_users", blank=True
    )

    interested_houses = models.ManyToManyField(
        House, related_name="interested_users", blank=True
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["email", "nickname"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.nickname

    def get_short_name(self):
        return self.nickname


class VerificationToken(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=127, unique=True)
    type_options = [("EMAIL", "EMAIL"), ("PASSWORD", "PASSWORD")]
    verification_type = models.CharField(max_length=10)
    timestamp = models.IntegerField()
    used = models.IntegerField(default=1)

    def __str__(self):
        return f"Token for {self.email} - {self.token}"
