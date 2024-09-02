from django.urls import path
from .import views 
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, ListAcceptedFriendsView, ListPendingFriendRequestsView


urlpatterns = [
    path('register/', views.register, name="register"),
    #path('me/', views.current_user, name="current_user"),
    path('search-users/', views.user_search_view, name='user-search'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/reject/<int:pk>/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/', ListAcceptedFriendsView.as_view(), name='list-friends'),
    path('friend-request/pending/', ListPendingFriendRequestsView.as_view(), name='list-pending-friend-requests'),
]

