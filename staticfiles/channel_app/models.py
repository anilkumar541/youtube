from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from coreapp.models import user_directory_path


User=settings.AUTH_USER_MODEL


STATUS=(
        ("Active", "Active"),
        ("Disabled", "Disabled"),
    )

# def user_directory_path(instance, filename):
#     return f"user_{instance.channel.user.id}/{filename}"

def user_directory_path(instance, filename):
    # Check that the instance has a channel attribute
    if hasattr(instance, 'channel') and instance.channel:
        user_id = instance.channel.user.id
    else:
        # If the instance does not have a channel attribute or it is None, use a default user ID
        user_id = 'default'

    # Construct the path using the user ID and filename
    return f"user_{user_id}/{filename}"



class Channel(models.Model):
    channel_art=models.ImageField(upload_to=user_directory_path, null=True, blank=True) #image for channel profile visit
    image=models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    full_name=models.CharField(max_length=150)
    channel_name=models.CharField(max_length=150, null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    keywords= TaggableManager()
    joined=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=STATUS, max_length=100, default="Active")
    user=models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="channel")
    subscribers=models.ManyToManyField(User, related_name="user_subs", blank=True)
    verified= models.BooleanField(default=False)
    total_views= models.IntegerField(default=0)

    business_email=models.EmailField(null=True, blank=True)
    make_business_email_public= models.BooleanField(default=False)

    business_location=models.CharField(max_length=500, null=True, blank=True)
    make_business_location_public= models.BooleanField(default=False)

    website= models.URLField(default= "https://www.mywebsite.com")
    linkedin= models.URLField(default= "https://www.linkedin.com")
    instagram= models.URLField(default= "https://www.instagram.com")
    twitter= models.URLField(default= "https://www.twitter.com")



    def __str__(self) -> str:
        return self.channel_name
        


# model for community post
class Community(models.Model):
    channel= models.ForeignKey(Channel, on_delete=models.CASCADE)
    image= models.ImageField(upload_to= user_directory_path, null= True, blank=True)
    content= models.TextField(null= True, blank= True)
    date= models.DateTimeField(auto_now_add= True)
    status= models.CharField(max_length= 100, choices= STATUS, default="Active")
    likes= models.ManyToManyField(User)

    def __str__(self) -> str:
        return self.channel.channel_name
    
    class Meta:
        verbose_name= "Community"  
        db_table="comminities"


# model for community post comment
class CommunityComment(models.Model):
    community= models.ForeignKey(Community, on_delete=models.CASCADE, related_name="comments")
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.CharField(max_length= 10000, null=True, blank= True)
    date= models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default= True)


    def __str__(self) -> str:
        return self.community.channel.channel_name
    
    class Meta:
        verbose_name= "Community Comments"  
        db_table="comminity_comments"



