from django.test import TestCase
from .models import Image,User
import datetime as dt



class ImageTestClass(TestCase):
  
    def setUp(self):
        self.user1 = User(username="laetitia")
        self.user1.save()
        self.image = Image(image='amezing',name='laetitia',caption='bad',profile=self.user1)

  
    def test_instance(self):
        self.assertTrue(isinstance(self.image,  Image))

  
    def test_save_method(self):
        self.image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images)>0)

   
    def test_delete_method(self):
        self.image2 = Image(image='Laetitia1',name='computer',caption="none",profile=self.user1)
        self.image2.save_image()
        self.image.save_image()
        self.image.delete_image()
        images = Image.objects.all()
        self.assertEqual(len(images),1)
   
class Profiletest(TestCase):
   

    def setUp(self):
        self.tempprofiles = []
        for i in range(self.users):
            tmp = Profile()
            tmp.save()
            self.tempprofiles.append(tmp)

    def test_follow(self):
        follower = Profile()
        follower.save()
        for i in self.tempprofiles:
            follower.follow(i)
            self.assertEquals(follower.following.count(), self.users)
        for u in self.tempprofiles:
            self.assertEquals(u.followers.count(), 1)