from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from posts.models import Post, Like, Comment, Follow, Story, Message

@staff_member_required
def admin_dashboard_page(request):
    context = {
        "users_count": User.objects.count(),
        "posts_count": Post.objects.count(),
        "likes_count": Like.objects.count(),
        "comments_count": Comment.objects.count(),
        "follows_count": Follow.objects.count(),
        "stories_count": Story.objects.count(),
        "messages_count": Message.objects.count(),
        "recent_users": User.objects.order_by("-date_joined")[:5],
        "recent_posts": Post.objects.order_by("-created_at")[:5],
    }
    return render(request, "dashboard/admin_dashboard.html", context)