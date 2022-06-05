from multiprocessing.dummy import current_process
import threading
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse

from . import settings
from .forms import UpdateUserForm, UpdateProfileForm, AddPostForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import Follow, Like, Post, Profile, Comment
from django.core.mail import EmailMessage


# Create your views here.

def welcome(request):
    posts = Post.objects.order_by('-date_created').all()
    profiles = Profile.objects.all()
    return render('Welcome to my insta clone')