from multiprocessing.dummy import current_process
import threading
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse

# from Instagram import settings
# from .forms import UpdateUserForm, UpdateProfileForm, AddPostForm
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.template.loader import render_to_string
# # from .tokens import account_activation_token
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
from .models import Follow, Like, Post, Profile, Comment
from django.core.mail import EmailMessage


# Create your views here.




def welcome(request):
    posts = Post.objects.order_by('-date_created').all()
    profiles = Profile.objects.all()
    return render(request, 'index.html', {'posts':posts, 'profiles':profiles})


def UserProfile(request, username):
    current_user = request.user
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    images = Post.objects.filter(author = profile.id).all()
    images_count = Post.objects.filter(author = profile.id)
    followers = Profile.get_followers(self=profile)
    following = Profile.get_following(self=profile)
    is_followed = False
    if followers.filter(user_id=current_user.id).exists() or following.filter(user_id=current_user.id).exists():
        is_followed=True
    else:
        is_followed=False
    return render(request, 'user_profile.html', {'profile':profile, 'profile_details':profile_details, 'images':images, 'images_count':images_count, 'followers':followers, 'following':following, 'current_user':current_user, 'is_followed':is_followed})


def MyProfile(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    images = Post.objects.filter(author = profile.id).all()
    images_count = Post.objects.filter(author = profile.id)
    followers = Profile.get_followers(self=profile)
    following = Profile.get_following(self=profile)
    return render(request, 'my_profile.html', {'profile':profile, 'profile_details':profile_details, 'images':images, 'images_count':images_count, 'followers':followers, 'following':following})


def EditProfile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Your Profile Has Been Updated Successfully!')
            return redirect('MyProfile', username=username)
        else:
            messages.error(request, "⚠️ Your Profile Wasn't Updated!")
            return redirect('EditProfile', username=username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


# def Settings(request, username):
#     username = User.objects.get(username=username)
#     if request.method == "POST":
#         form = PasswordChangeForm(data=request.POST, user=request.user)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             messages.success(request, '✅ Your Password Has Been Updated Successfully!')
#             return redirect("MyProfile", username=username)
#         else:
#             messages.error(request, "⚠️ Your Password Wasn't Updated!")
#             return redirect("Settings", username=username)
#     else:
#         form = PasswordChangeForm(data=request.POST, user=request.user)
#         return render(request, "settings.html", {'form': form})

def SingleImage(request, id):
    post = Post.objects.get(id = id)
    print(post)
    likes = Like.objects.filter(post = post.id).count()
    print(likes)
    comments = Comment.objects.filter(post = post.id).count()
    print(comments)
    return render(request, 'Post Details.html', {'post': post, 'comments':comments, 'likes':likes})


def AddNewPost(request, username):
    form = AddPostForm()
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.profile = request.user.profile
            post.save()
            messages.success(request, '✅ Your Post Was Created Successfully!')
            return redirect('MyProfile', username=username)
        else:
            messages.error(request, "⚠️ Your Post Wasn't Created!")
            return redirect('AddNewPost', username=username)
    else:
        form = AddPostForm()
    return render(request, 'post.html', {'form':form})


def AddComment(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        usercomment = request.POST['comment']
        comment_obj = Comment.objects.create(opinion = usercomment, author = request.user, post = post)
        comment_obj.save()
        messages.success(request, '✅ Your Comment Was Created Successfully!')
        return redirect('welcome')
    else:
        messages.error(request, "⚠️ Your Comment Wasn't Created!")
        return redirect('welcome')


def PostLike(request,id):
    postTobeliked = Post.objects.get(id = id)
    currentUser = User.objects.get(id = request.user.id)
    if not postTobeliked:
        return "Post Not Found!"
    else:
        like = Like.objects.filter(author = currentUser, post = postTobeliked)
        if like:
            messages.error(request, '⚠️ You Can Only Like A Post Once!')
            return redirect('welcome')
        else:
            likeToadd = Like(author = currentUser, post = postTobeliked)
            likeToadd.save()
            messages.success(request, '✅ You Successfully Liked The Post!')
            return redirect('welcome')


def FollowUser(request, username):
    userTobefollowed = User.objects.get(username = username)
    currentUser = request.user
    is_followed = False
    if userTobefollowed.id == currentUser.id:
        messages.error(request, "⚠️ You can't follow yourself!")
        return redirect('UserProfile', username=username)
    if not userTobefollowed:
        messages.error(request, "⚠️ User Does Not Exist!")
        return redirect('UserProfile', username=username)
    else:
        follow = Follow.objects.filter(user = currentUser, following = userTobefollowed)
        if follow:
            messages.error(request, '⚠️ You Can Only Follow A User Once!')
            return redirect('UserProfile', username=username)
        else:
            folowerToadd = Follow(user = currentUser, following = userTobefollowed)
            folowerToadd.save()
            messages.success(request, "✅ You Are Now Following This User!")
            return redirect('UserProfile', username=username)

# will add the search function here
def SearchUsers(request):
  if 'username' in request.GET and request.GET["username"]:
      search_term = request.GET.get("username")
      searched_users = Profile.search_by_profile(search_term)
      message = f"{search_term}"
      return render(request, "search.html",{"message":message,"users": searched_users})
  else:
      message = "You haven't searched for any term"
      return render(request, 'search.html',{"message":message})