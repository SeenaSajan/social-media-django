from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post, Like, Comment, Follow, Story
from posts.forms import PostForm, StoryForm
from posts.models import Message

@login_required(login_url='login')
def profile_page(request):
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')

    followers_count = Follow.objects.filter(following=request.user).count()
    following_count = Follow.objects.filter(follower=request.user).count()

    return render(request, "social/profile.html", {
        "user_posts": user_posts,
        "followers_count": followers_count,
        "following_count": following_count
    })

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect('feed')

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        text = request.POST.get("comment")

        post = Post.objects.get(id=post_id)

        Comment.objects.create(
            user=request.user,
            post=post,
            text=text
        )

    return redirect("feed")


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("profile")

    return render(request, "social/delete_post.html", {"post": post})



@login_required
def follow_user(request, username):
    target_user = User.objects.get(username=username)

    if request.user != target_user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            follow.delete()

    return redirect('user_profile', username=username)

@login_required(login_url='login')
def user_profile(request, username):
    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(user=user).order_by('-created_at')

    is_following = Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()

    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    return render(request, "social/user_profile.html", {
        "profile_user": user,
        "user_posts": user_posts,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count
    })

@login_required(login_url='login')
def feed_page(request):
    posts = Post.objects.all().order_by('-created_at')
    stories = Story.objects.all().order_by('-created_at')
    form = PostForm()
    story_form = StoryForm()

    liked_posts = []
    for post in posts:
        if post.like_set.filter(user=request.user).exists():
            liked_posts.append(post.id)

    if request.method == 'POST':
        if 'post_submit' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('feed')

        elif 'story_submit' in request.POST:
            story_form = StoryForm(request.POST, request.FILES)
            if story_form.is_valid():
                story = story_form.save(commit=False)
                story.user = request.user
                story.save()
                return redirect('feed')

    return render(request, "social/feed.html", {
        'posts': posts,
        'stories': stories,
        'form': form,
        'story_form': story_form,
        'liked_posts': liked_posts
    })

def post_view_page(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "social/post_view.html", {'post': post})

@login_required(login_url='login')
def story_viewer_page(request, story_id):
    story = Story.objects.get(id=story_id)
    return render(request, "social/story_viewer.html", {'story': story})

@login_required
def chat_list_page(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "social/chat_list.html", {"users": users})


@login_required
def chat_room_page(request, user_id):
    other_user = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == "POST":
        text = request.POST.get("message")
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text
            )
        return redirect('chat_room', user_id=other_user.id)

    return render(request, "social/chat_room.html", {
        "other_user": other_user,
        "messages": messages
    })
@login_required(login_url='login')
def stories_page(request):
    stories = Story.objects.all().order_by('-created_at')
    story_form = StoryForm()

    if request.method == 'POST':
        story_form = StoryForm(request.POST, request.FILES)
        if story_form.is_valid():
            story = story_form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('stories_page')

    return render(request, "social/stories.html", {
        "stories": stories,
        "story_form": story_form
    })