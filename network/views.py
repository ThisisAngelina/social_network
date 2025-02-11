from webbrowser import get
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post, Following
from .forms import PostForm

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

def home(request):
    ''' Allow an authenticated user to publish a post and all users to view posts'''
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            form = PostForm(request.POST)

            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = user
                new_post.save()
                messages.success(request, "Hooray! Your post was saved!")
                return redirect('home')
            messages.warning(request, "Oops! Something went wrong! Please try again.") # form was not valid
        else: #user is not authenticated
            messages.warning(request, "Please log in to publish posts")
            return redirect('home')
    else:
        form = PostForm()
        posts = Post.objects.all()
        paginator = Paginator(posts, 10)  # display 10 posts at a time
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/home.html', {'form': form, 'page_obj': page_obj})

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)

    paginator = Paginator(posts, 10)  # display 10 posts at a time
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/profile.html', {'profile_user':user, 'page_obj': page_obj})

@login_required
def follow(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    if profile_user is not None:
        follow_relation, created = Following.objects.get_or_create(follower=request.user, followed=profile_user)

        if not created: # the user was already following that profile
            follow_relation.delete()  # Unfollow if already following
        
        unfollow_option = created  # Now that the user follows this profile, give them the option to unfollow it

        # Send back the updated button as an HTMX response
        button_html = f'''
            <button class="btn {"btn-danger" if unfollow_option else "btn-primary"}"
                    hx-post="/follow/{profile_user.id}/"
                    hx-target="#follow-btn"
                    hx-swap="outerHTML"
                    id="follow-btn">
                {"Unfollow" if unfollow_option else "Follow"}
            </button>
        '''
        
        following_result = "followed" if unfollow_option else "unfollowed" # for the message
        messages.success(request, f"Success! You have {following_result} {profile_user.username}!")
        return HttpResponse(button_html)

    else: # the profile user was not found
        messages.warning(request, "Oops! Something went wrong! Please try again.")
        return redirect('profile', user_id=user_id)
        

@login_required
def followed_posts(request):
    followed_users = Following.objects.filter(follower=request.user).values_list('followed', flat=True)
    followed_posts = Post.objects.filter(user__in=followed_users).order_by('-timestamp')

    paginator = Paginator(followed_posts, 10)  # display 10 posts at a time
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/followed_posts.html', {'page_obj': page_obj})

@login_required
def edit_post(request, post_id):
    ''' alow the user to request to edit a particular post '''

    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:  # Ensure only the owner can edit
        messages.warning(request, "Oops, you cannot edit this post!")
        return HttpResponse("Unauthorized", status=403)

    form = PostForm(instance=post) # prefill the edit form with the existing data saved in the model instance

    return render(request, "network/partials/edit_post.html", {"form": form, "post": post})


@login_required
def save_post(request, post_id):
    ''' alow the user to save the edited post '''

    print('the save button was pressed')
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # save the model instance with the data passed through the form

        if form.is_valid():
            form.save()
            messages.success(request, "Your post was successfully edited")

            # Return the updated post HTML
            return render(request, "network/partials/post.html", {"post": post})

    messages.warning(request, "Error updating post")
    return HttpResponse("Invalid Request", status=400)


@login_required
def like(request, post_id):
    pass
# aslo need to implement UNLIKE
# add htmx to the like button
# when a person has liked a post, send back html of an unlike button 
#  

@login_required
def comment(request, post_id):
    pass