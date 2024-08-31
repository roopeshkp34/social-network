from django.urls import path

from friends import views

urlpatterns = [
    path("friend-request", views.FriendRequestView.as_view(), name="send request"),
    path(
        "friend-request/<str:pk>/accept",
        views.AcceptFriendRequestView.as_view(),
        name="accept friend request",
    ),
    path(
        "friend-request/<str:pk>/reject",
        views.RejectFriendRequestView.as_view(),
        name="reject friend request",
    ),
    path("friends-list", views.ListFriendsView.as_view(), name="list friends"),
    path("pending-requests", views.ListPendingRequestView.as_view(), name="list pending requests")
]
