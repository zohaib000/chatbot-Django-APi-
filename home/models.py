from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models

# Create your models here.
status = (
    ('pending', 'pending'),
    ('completed', 'completed')
)


class credits(models.Model):
    available = models.IntegerField()
    user = models.CharField(max_length=400)
    date = models.DateField(auto_now_add=True)


class categories(models.Model):
    name = models.CharField(max_length=500)


class ProfileData(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    picture = models.ImageField(
        upload_to="profile_images", blank=True, null=True, default="profile_images/default.png")
    email = models.CharField(max_length=400)
    account = models.CharField(max_length=400)


class Chat(models.Model):
    name = models.CharField(max_length=300)
    user = models.CharField(max_length=300)
    prompt_title = models.CharField(max_length=300)
    prompt_id = models.CharField(max_length=300)
    # includes json of {query,response} in list of objects
    chat = models.TextField()


class savedPrompts(models.Model):
    Title = models.CharField(max_length=500)
    pid = models.CharField(max_length=500)  # ~ to save prompt id
    Description = models.TextField()
    prompt_text = models.TextField()
    Time = models.TimeField(blank=True, auto_now_add=True, null=True)
    Date = models.DateField(blank=True, auto_now_add=True, null=True)
    User = models.CharField(max_length=500)
    Views = models.CharField(
        max_length=100000, default=0, null=True, blank=True)
    saved_by = models.CharField(max_length=1000)
    img = models.ImageField(
        upload_to="savedPrompts Images", blank=True, null=True, default="profile_images/default.png")

    user_img = models.ImageField(
        upload_to="userImages", blank=True, null=True, default="profile_images/default.png")
    category = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        user_pic = ProfileData.objects.filter(
            email=str(self.User)).last().picture
        self.user_img = user_pic
        super(savedPrompts, self).save(*args, **kwargs)

    def __str__(self):
        return self.Title


class Prompt(models.Model):
    Title = models.CharField(max_length=500)
    Description = models.TextField()
    prompt_text = models.TextField()
    Time = models.TimeField(blank=True, auto_now_add=True)
    Date = models.DateField(blank=True, auto_now_add=True)
    User = models.CharField(max_length=500)
    Views = models.CharField(
        max_length=100000, default=0, null=True, blank=True)
    img = models.ImageField(
        upload_to="Prompts Images", blank=True, null=True, default="profile_images/default.png")
    user_img = models.ImageField(
        upload_to="userImages", blank=True, null=True, default="profile_images/default.png")

    def save(self, *args, **kwargs):
        user_pic = ProfileData.objects.filter(
            email=str(self.User)).last().picture
        self.user_img = user_pic
        super(Prompt, self).save(*args, **kwargs)

    def __str__(self):
        return self.Title


class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @ property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
