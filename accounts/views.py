from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post
from django.shortcuts import get_object_or_404, redirect



def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return render(request, "accounts/signup.html", {"error": "Username already exists"})
            else:
                User.objects.create_user(username=username, email=email, password=password)
                return redirect("login")
        else:
            return render(request, "accounts/signup.html", {"error": "Passwords do not match"})

    return render(request, "accounts/signup.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("/dashboard/admin/")
            else:
                return redirect("feed")
        else:
            return render(request, "accounts/login.html", {"error": "Invalid username or password"})

    return render(request, "accounts/login.html")

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/update_profile.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect("login")


def profile_page(request, username):
    return render(request, "accounts/user_profile.html", {"username": username})


def edit_profile_page(request, username):
    return render(request, "accounts/edit_profile.html", {"username": username})

from django.shortcuts import redirect

def redirect_after_login(request):
    if request.user.is_staff:
        return redirect('/dashboard/admin/')
    else:
        return redirect('/')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.caption = request.POST.get("caption")

        if request.FILES.get("image"):
            post.image = request.FILES.get("image")

        post.save()
        return redirect("profile")

    return render(request, "social/edit_post.html", {"post": post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()

    return redirect("profile")