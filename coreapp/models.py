from django.db import models
from taggit.managers import TaggableManager
# from userauthentication_app.models import User
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



User=settings.AUTH_USER_MODEL

def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"

class Video(models.Model):
    visibility=(
        ("Private", "Private"),
        ("Unlisted", "Unlisted"),
        ("Members Only", "Members Only"),
        ("Public", "Public"),
    )

    video=models.FileField(upload_to=user_directory_path)
    image=models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    title=models.CharField(max_length=150)
    description=models.TextField(null=True, blank=True)
    tags= TaggableManager()
    date=models.DateTimeField(auto_now_add=True)
    visibility=models.CharField(choices=visibility, max_length=100, default="Public")
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    views=models.PositiveIntegerField(default=0)
    likes= models.ManyToManyField(User, related_name="likes")

    # adding featured field to show the video on top of channel profile
    featured= models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        print(*args, "jkasndj")
        print(**kwargs)
        if self.image:
            # Open the image using PIL
            img = Image.open(self.image)

            # If the image is larger than 1MB, resize it
            # print(self.image.size, "before")
            if self.image.size > 1024 * 1024:
                img.thumbnail((1024, 1024))

                # Save the resized image to memory
                output = BytesIO()
                img.save(output, format='JPEG', quality=80)
                output.seek(0)

                # Set the file attributes for the resized image
                file = InMemoryUploadedFile(output, 'ImageField', f'{self.image.name.split(".")[0]}_resized.jpg',
                                            'image/jpeg', output.getbuffer().nbytes, None)

                # Replace the original image with the resized image
                self.image = file

        # print(self.image.size, "after")
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.title
        

# model for comments
class Comment(models.Model):
    comment= models.CharField(max_length=1000)
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    active= models.BooleanField(default=True)
    video= models.ForeignKey(Video, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.comment[:30]


