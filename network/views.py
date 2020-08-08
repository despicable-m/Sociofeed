from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like

dt = datetime.now()
d = dt.date()
t = dt.strftime("%H:%M:%S")


def index(request):
    if request.method == "POST":
        post = request.POST["post"]
        user = request.user

        Post.objects.create(user=user, post=post, date=d, time=t)

    post = Post.objects.all()
    # post = reversed(post)

    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "post":post
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request):
    user = User.objects.get(username=request.user)
    users = User.objects.exclude(username=request.user)
    posts = Post.objects.filter(user=user)
    # posts = reversed(posts)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user":user,
        "posts":posts,
        "users":users
    })


def follow(request, id):
    curr_user = User.objects.get(username=request.user)
    f = User.objects.get(pk=id)
    g = f.followers.all()

    g_list = list()
    for user in g:
        g_list.append(user.follow.username)

    if str(curr_user) in g_list:
        Follow.objects.get(follow=curr_user, followee=f).delete()
    else:
        Follow.objects.create(follow=curr_user, followee=f)
        
    return HttpResponseRedirect(reverse("profile"))

def following(request):
    u = User.objects.get(username=request.user)
    p = Post.objects.all()
    f_users = u.following.all()

    users = list()
    for i in f_users:
        users.append(i.followee)
    
    posts = list()
    for i in users:
        p = Post.objects.filter(user=i)

        for post in p:
            posts.append(post)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts":posts
    })


def edit(request, id):
    if request.method == "POST":
        post = request.POST["post"]

        p = Post.objects.get(pk=id)
        if p.user != request.user:
            return HttpResponse("Sorry, you can't edit others' posts")
        
        p.post = post
        p.save()

        return HttpResponseRedirect(reverse("index"))

    p = Post.objects.get(pk=id)
    
    if p.user == request.user:
        return render(request, "network/edit.html",{
            "p":p
        })
    else:
        return HttpResponse("Sorry, you can't edit others' posts")


def like(request, id):
    user = User.objects.get(username=request.user)
    post = Post.objects.get(pk=id)
    post_likes = post.likes.all()
    
    liker_list = list()
    for likes in post_likes:
        liker_list.append(likes.user.username)

    if str(request.user) in liker_list:
        Like.objects.filter(user=user, post=post).delete()
    else:
        Like.objects.create(user=user, post=post, like=1)
    return HttpResponseRedirect(reverse("index"))