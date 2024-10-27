from django.urls import path
from . import views

urlpatterns = [
    path("post/", views.PostListCreateView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/like/<int:pk>/", views.PostLikeView.as_view(), name="post-like"),
    path("user/follow/<int:pk>/", views.UserFollowView.as_view(), name="user-follow"),
    path("user/follower/<int:pk>/", views.UserFollowerListView.as_view(), name="user-follower"),
    path("user/following/<int:pk>/", views.UserFollowingListView.as_view(), name="user-following"),
    path("profile/", views.ProfileListView.as_view(), name="profile"),
]