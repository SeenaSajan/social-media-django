from django.urls import path
from . import views

urlpatterns = [
    path("admin/", views.admin_dashboard_page, name="admin_dashboard"),
]