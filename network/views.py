from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post
from .forms import PostCreateForm

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "network/register.html")


#@login_required #TODO POST only if authenticated, GET for everyone
def home(request):
    ''' Allow an authenticated user to publish a post and all users to view posts'''
    if request.method == 'POST':
        user = request.user
        form = PostCreateForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = user
            new_post.save()
            messages.success(request, "Hooray! Your post was saved!")
            return redirect('home')
        messages.error(request, "Oops! Something went wrong! Please try again.") # form was not valid
    else:
        form = PostCreateForm()
        posts = Post.objects.all()
        return render(request, 'network/home.html', {'form': form, 'posts': posts})

