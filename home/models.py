from django.db import models
from login.models import UserProfile
from django.conf import settings
#from django.contrib.auth import timezone

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null = True,  on_delete=models.CASCADE)
    post = models.CharField(max_length=500 ,blank=False)
    
    image1 = models.ImageField(null = True,  blank=False, upload_to='posts/%Y/%m/%d')
    image2 = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
    image3 = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
    image4 = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
    
    #view = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="likes", null=True)
    likes = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    
    date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.post

    def total_likes(self):
        return self.likes.count()


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="owner", null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend,created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend,created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)
    
    def __str__(self):
        return str(self.current_user)
    

# Create your models here.
class Create(models.Model):
    Bizname = models.CharField(max_length=200)
    Location = models.TextField()
    Phone = models.CharField(max_length=14)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    #created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Bizname 


class Aboutpage(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=700,blank=True)
    image = models.ImageField(upload_to='aboutpage/%Y/%m/%d', blank=True)
    image1 = models.ImageField(upload_to='aboutpage/%Y/%m/%d', blank=True)

    aboutus = models.TextField(max_length=500, blank=True)
    aboutimage = models.ImageField(upload_to='aboutpage/%Y/%m/%d', blank=True)

    project = models.TextField(max_length=500, blank=True)
    projectimage = models.ImageField(upload_to='aboutpage/%Y/%m/%d', blank=True)

    story = models.TextField(max_length=1500, blank=True)
    storyimage = models.ImageField(upload_to='aboutpage/%Y/%m/%d', blank=True)

    team = models.TextField(max_length=1500, blank=True)
    teamimage = models.ImageField(upload_to='aboutpage/%Y/%m/%d', blank=True)
    whyus = models.TextField(max_length=1500, blank=True)
    whyusimage = models.ImageField(upload_to='aboutpage/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email