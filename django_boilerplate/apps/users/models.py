from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

from apps.utils.models import BaseModel, Activable


class UserManager(BaseUserManager):
    """Custom manager for the User model."""

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given username and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """
        Create and save a regular User with the given username and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser, BaseModel, Activable):
    """
    Custom User model for the project. Uses 'username' as the unique identifier.

    Attributes:
        - phone_number: E.164 format phone number (validated).
        - dob: Date of birth of the user.
        - profile_picture: Optional profile picture.
        - email_verified: Status flag for email verification.
        - gender: Gender selection field with predefined choices.
    """

    objects = UserManager()

    class UserGender(models.TextChoices):
        UNSPECIFIED = ("unspecified", "Unspecified")
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    email = None
    #email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=150, unique=True, verbose_name="username")
    USERNAME_FIELD = "username" 
    REQUIRED_FIELDS = []
    

    dob = models.DateField(null=True, blank=True, verbose_name="date of birth")
    profile_picture = models.ImageField(blank=True, upload_to="user/profile_picture/")
    email_verified = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=50,
        choices=UserGender.choices,
        default=UserGender.UNSPECIFIED,
        verbose_name="gender",
    )

    def __str__(self):
        return f"user-{self.username}"

    @property
    def full_name(self):
        """
        Return the user's full name.
        """
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age(self):
        """
        Calculate and return the user's age based on their date of birth.
        """
        return (
            round((timezone.localdate() - self.dob).days / 365)
            if self.dob
            else None
        )
