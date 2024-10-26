from django.urls import path
from . import views

urlpatterns = [
    path("post/", views.PostListCreateView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
]