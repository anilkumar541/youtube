from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from coreapp.models import Video


class User(AbstractUser):
    email= models.EmailField(unique=True, null=True)
    username=models.CharField(max_length=100)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return self.username


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    saved_videos= models.ManyToManyField(Video,  blank= True)

    def __str__(self):
        return self.user.username


# use signals for when user is created then profile of user should  also be created 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user =instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender = User)
post_save.connect(save_user_profile, sender = User)