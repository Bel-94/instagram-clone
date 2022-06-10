from django import forms
from .models import Post, Profile, Follow, Comment
from django.forms import ModelForm


class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["created", "account_holder", "followers", "following"]


class UploadImageForm(ModelForm):
    class Meta:
        model = Post
        exclude = ["profile", "post_date", "likes"]


class EditBioForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]


class FollowForm(ModelForm):
    class Meta:
        model = Follow
        exclude = ["followed", "follower"]


class UnfollowForm(ModelForm):
    class Meta:
        model = Follow
        exclude = ["followed", "follower"]


# comment form
