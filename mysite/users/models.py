from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pic = Image.open(self.image.path)

        if pic.height > 300 or pic.width > 300:
            resize = (300, 300)
            pic.thumbnail(resize)
            pic.save(self.image.path)
    

