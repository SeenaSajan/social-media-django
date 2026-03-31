from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed_page, name="feed"),
    path("post/<int:post_id>/", views.post_view_page, name="post_view"),
    path("stories/<int:story_id>/", views.story_viewer_page, name="story_viewer"),
    path("chats/", views.chat_list_page, name="chat_list"),
    path("profile/", views.profile_page, name="profile"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("delete-post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("chats/", views.chat_list_page, name="chat_list"),
    path("chats/<int:user_id>/", views.chat_room_page, name="chat_room"),
    path("stories/", views.stories_page, name="stories_page"),
    
]