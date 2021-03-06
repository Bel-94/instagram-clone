from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from .forms import *
from .models import *
from .email import send_welcome_email



# Create your views here.

@login_required(login_url="/accounts/login/")
def create_profile(request):
    current_user = request.user
    if request.method == "POST":
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()

        return HttpResponseRedirect("/")

    else:
        form = CreateProfileForm()
    return render(request, "main/create_profile.html", {"form": form})


@login_required(login_url="/accounts/login/")
def home(request):
    current_user = request.user
    print(current_user.profile.id)
    
    try:
        logged_in = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        raise Http404()

    logged_in = Profile.objects.get(user=current_user)
    timeline_images = []
    current_images = Post.objects.filter(profile=logged_in)
    for current_image in current_images:
        timeline_images.append(current_image.id)

    current_following = Follow.objects.filter(follower=logged_in)
    for following in current_following:
        following_profile = following.followed
        following_images = Post.get_profile_images(following_profile)
        for image in following_images:
            timeline_images.append(image.id)

    display_images = Post.objects.filter(id=request.user.id).order_by("-date_created")
    timeline = Post.objects.filter(pk__in=timeline_images).order_by("-date_created")

    liked = False
    for i in display_images:
        image = Post.objects.get(pk=i.id)
        liked = False
        if image.likes.filter(pk__in=timeline_images).exists():
            liked = True

    comments = Comment.objects.all()
    comments_count  = comments.count()   #changed here to check incase i get an error

    suggestions = Profile.objects.all()

    context={

        "images": display_images,
            "suggestions": suggestions,
            "loggedIn": logged_in,
            "liked": liked,
            "comments": comments,
            "timeline": timeline,
    }

    return render(request,"main/home.html", context=context)


@login_required(login_url="/accounts/login/")
def upload_image(request):
    title = "Upload image"
    current_user = request.user
    try:
        profile = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        raise Http404()
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = profile
            image.save()
        return redirect("home")
    else:
        form = UploadImageForm()
    return render(request, "main/upload_image.html", {"form": form, "title": title})

# def profile(request):
#     current_user = request.user
#     user = User.objects.get(id = current_user.id)
#     posts = Post.objects.filter(user = user.id)
#     follow = Follow.objects.filter(follower_id = user.id)
#     profile=Profile.filter_profile_by_id(user.id) 

#     ctx = {
#         "posts":posts,
#         "profile":profile,
#         'user':user,
#         'follow':follow
#         }  
#     return render(request, 'profile/profile.html',ctx)

def profile(request, profile_id):
    title = "Profile"
    current_user = request.user
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        raise Http404()
    try:
        profile_following = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        raise Http404()
    try:
        profile_followed = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        if "follow" in request.POST:
            form = FollowForm(request.POST)
            if form.is_valid():
                this_follow = form.save(commit=False)
                this_follow.followed = profile_followed
                this_follow.follower = profile_following
                this_follow.save()
                set_of_followers = Follow.objects.filter(followed=profile_followed)
                num_of_followers = len(set_of_followers)
                profile_followed.followers = num_of_followers
                profile_followed.save()
                set_of_following = Follow.objects.filter(follower=profile_following)
                num_of_following = len(set_of_following)
                profile_following.following = num_of_following
                profile_following.save()
            return HttpResponseRedirect(f"/profile/{profile_id}")

        elif "unfollow" in request.POST:
            form = UnfollowForm(request.POST)
            if form.is_valid():
                this_unfollow = form.save(commit=False)     #check on this later
                is_unfollow = Follow.objects.filter(
                    followed=profile_followed, follower=profile_following
                )
                is_unfollow.delete()
                set_of_followers = Follow.objects.filter(followed=profile_followed)
                num_of_followers = len(set_of_followers)
                profile_followed.followers = num_of_followers
                profile_followed.save()
                set_of_following = Follow.objects.filter(follower=profile_following)
                num_of_following = len(set_of_following)
                profile_following.following = num_of_following
                profile_following.save()
            return HttpResponseRedirect(f"/profile/{profile_id}")
    else:
        form_follow = FollowForm()
        form_unfollow = UnfollowForm()

    images = Post.objects.filter(profile=profile).order_by("-date_created")
    images = Post.get_profile_images(profile=profile)
    images = Post.objects.filter(profile=profile).order_by("-date_created")
    posts = images.count()

    is_following = Follow.objects.filter(
        followed=profile_followed, follower=profile_following
    )
    comments = Comment.objects.order_by("-pub_date")

    if is_following:
        return render(
            request,
            "profile/profile.html",
            {
                "profile": profile,
                "images": images,
                "comments": comments,
                "unfollow_form": form_unfollow,
                "posts": posts,
                "title": title,
            },
        )

    return render(
        request,
        "profile/profile.html",
        {
            "profile": profile,
            "images": images,
            "comments": comments,
            "follow_form": form_follow,
            "posts": posts,
            "title": title,
        },
    )


def comment(request, image_id):
    image = Post.objects.get(pk=image_id)
    content = request.GET.get("comment")
    print(content)
    user = request.user
    comment = Comment(content=content, user=user)
    comment.save_comment()

    return redirect("home")


# def comment(request,post_id):
#     current_user = request.user
#     if request.method == 'POST':
#         comment= request.POST.get('comment')
#     post = Post.objects.get(id=post_id)
#     user_profile = User.objects.get(username=current_user.username)
#     Comment.objects.create(
#          comment=comment,
#          post = post,
#          user=user_profile   
#         )
#     return redirect('Home' ,pk=post_id)





# def update_profile(request,id):
#     user = User.objects.get(id=id)
#     profile = Profile.objects.get(user = user)
#     if request.method == "POST":
#             form = EditBioForm(request.POST,request.FILES,instance=profile)
#             if form.is_valid():
#                 form.save()
#                 return redirect('profile') 
#             else:
#                 return render(request,'main/edit_profile.html',{'form':form})
#     else:        
#         form = EditBioForm(instance=profile)
#     return render(request, 'main/edit_profile.html', {'form':form})


def profile_edit(request):
    current_user = request.user
    if request.method == "POST":
        form = EditBioForm(request.POST, request.FILES)
        if form.is_valid():
            profile_pic = form.cleaned_data["profile_image"]
            bio = form.cleaned_data["bio"]
            updated_profile = Profile.objects.get(user=current_user)
            updated_profile.profile_image = profile_pic
            updated_profile.bio = bio
            updated_profile.save()
        return redirect("profile")
    else:
        form = EditBioForm()
    return render(request, "main/edit_profile.html", {"form": form})

@login_required(login_url="/accounts/login/")
def search(request):
    if "search_user" in request.GET and request.GET["search_user"]:
        search = request.GET.get("search_user")
        searched_user = Profile.search_user(search)
        message = f"{search}"

        return render(
            request,
            "main/search.html",
            {"message": message, "searched_user": searched_user},
        )

    else:
        message = "You haven't searched for any term"
    return render(request, "main/search.html", {"message": message})


@login_required(login_url="/accounts/login/")
def email(request):
    current_user = request.user
    email = current_user.email
    name = current_user.username
    send_welcome_email(name, email)
    return redirect(create_profile)


def like_image(request, image_id):
    image = Post.objects.get(pk=image_id)
    liked = False
    current_user = request.user
    try:
        profile = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        raise Http404()
    if image.likes.filter(id=profile.id).exists():
        image.likes.remove(profile)
        liked = False
    else:
        image.likes.add(profile)
        liked = True
    return HttpResponseRedirect(reverse("home"))

def one_image(request, image_id):
    try:
        image=Post.objects.get(pk=image_id)
    except Post.DoesNotExist:
        raise Http404()

    return render(request, 'main/single_post.html',{"image":image})