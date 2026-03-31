from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("logout/", views.logout_page, name="logout"),
    path("profile/<str:username>/", views.profile_page, name="profile"),
    path("profile/<str:username>/edit/", views.edit_profile_page, name="edit_profile"),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),
]