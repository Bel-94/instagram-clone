from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    bio = models.TextField(max_length=150, verbose_name='Bio', null=True)
    profile_image = CloudinaryField('image')
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

        # @receiver(post_save, sender=User)

    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_user(cls, username):
        return User.objects.filter(username=username)

class Post(models.Model):
    image = CloudinaryField('image')
    title = models.CharField(max_length=30, null=False)
    caption = models.CharField(max_length=2200, null=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name="posts")

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def update_caption(self, new_caption):
        self.caption = new_caption
        self.save()

    def like_count(self):
        return self.likes.count()

    @classmethod
    def get_profile_images(cls, profile):
        return cls.objects.filter(profile=profile)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']


class Follow(models.Model):
    posted = models.DateTimeField(auto_now_add=True, null=True)
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_followed", default=0)
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_following", default=0)

    def __str__(self):
        return self.pk

class Comment(models.Model):
    content = models.TextField(max_length=150, null=True)
    pub_date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_post_comments(cls, image):
        return cls.objects.filter(image=image)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ["-pub_date"]
