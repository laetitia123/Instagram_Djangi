from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save

class Image(models.Model):
    name = models.CharField(max_length =60)
    caption= HTMLField()
    profile = models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'images/')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='images')
    @classmethod
    def todays_news(cls):
        today = dt.date.today()
        images = cls.objects.filter(pub_date__date = today)
        return images
    @classmethod
    def days_news(cls,date):
        news = cls.objects.filter(pub_date__date = date)
        return news
    @classmethod
    def search_by_title(cls,search_term):
        news = cls.objects.filter(title__icontains=search_term)
        return news

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    Name = models.TextField(default="Anonymous")
    profile_picture = models.ImageField(
        upload_to='users/', default='users/user.png')
    bio = models.TextField(default="Welcome Me!")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @classmethod
    def find_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

    def togglefollow(self, profile):
        if self.following.filter(followee=profile).count() == 0:
            Follows(followee=profile, follower=self).save()
            return True
        else:
            self.following.filter(followee=profile).delete()
            return False

    def like(self, photo):
        if self.mylikes.filter(photo=photo).count() == 0:
            Likes(photo=photo, user=self).save()

    def save_image(self, photo):
        if self.saves.filter(photo=photo).count() == 0:
            Saves(photo=photo, user=self).save()
        else:
            self.saves.filter(photo=photo).delete()

    def unlike(self, photo):
        self.mylikes.filter(photo=photo).all().delete()

    def comment(self, photo, text):
        Comment(text=text, photo=photo, user=self).save()

    def post(self, form):
        image = form.save(commit=False)
        image.user = self
        image.save()

    @property
    def follows(self):
        return [follow.followee for follow in self.following.all()] 
    def __str__(self):
        return self.user.username