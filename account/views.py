from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import SignUpSerializer, FriendRequestSerializer, UserSerializer, FriendListSerializer
from django.db.models import Q
from rest_framework import generics, status
from .models import FriendRequest
from datetime import timezone, timedelta
from datetime import datetime


# Create your views here.

# Sign UP 
@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():

            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password']),
            )

            return Response({ 'details': 'User Registered' }, status=status.HTTP_201_CREATED)

        else:
            return Response({ 'error': 'User already exists' }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


#Search for the user

class UserSearchPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_search_view(request):
    search_keyword = request.query_params.get('search', '')
    queryset = User.objects.all()

    if search_keyword:
        # Search by exact email
        email_match = queryset.filter(email__iexact=search_keyword) 
        if email_match.exists():
            queryset = email_match
        else:
            # Search by name containing the search keyword
            queryset = queryset.filter(
                Q(first_name__icontains=search_keyword) |
                Q(last_name__icontains=search_keyword) |
                Q(username__icontains=search_keyword)
            )

    #Paginate the queryset
    paginator = UserSearchPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    # Serialize the data
    serializer = UserSerializer(paginated_queryset, many=True)

    return paginator.get_paginated_response(serializer.data)



# View to send a friend request
class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        to_user = request.data.get('to_user')
        try:
            to_user_instance = User.objects.get(pk=to_user)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user_instance, status=FriendRequest.Status.PENDING).exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)

        
        recent_requests_count = FriendRequest.objects.filter(
            from_user=request.user, 
            timestamp__gte=one_minute_ago
        ).count()

        # Check if the user has exceeded the limit
        if recent_requests_count >= 3:
            return Response(
                {"detail": "You have exceeded the limit of 3 friend requests per minute."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        friend_request = FriendRequest(from_user=request.user, to_user=to_user_instance)
        friend_request.save()

        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)



# View to accept a friend request

class AcceptFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def update(self, request, *args, **kwargs):
        # Retrieve the friend request using the pk from the URL
        try:
            instance = self.get_object()
        except FriendRequest.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the current user is the intended recipient
        if instance.to_user != request.user:
            return Response({"detail": "You do not have permission to accept this request."}, status=status.HTTP_403_FORBIDDEN)

        # Ensure the friend request is pending before accepting
        if instance.status != FriendRequest.Status.PENDING:
            return Response({"detail": "Friend request is not in a pending state."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the status to ACCEPTED
        instance.status = FriendRequest.Status.ACCEPTED
        instance.save()

        return Response(FriendRequestSerializer(instance).data, status=status.HTTP_200_OK)


# View to reject a friend request

class RejectFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user:
            return Response({"detail": "You do not have permission to reject this request."}, status=status.HTTP_403_FORBIDDEN)
        
        instance.status = FriendRequest.Status.REJECTED
        instance.save()

        return Response(FriendRequestSerializer(instance).data)

#To List the Friends list

class ListAcceptedFriendsView(generics.ListAPIView):
    serializer_class = FriendListSerializer  # Use the serializer for User model
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        
        # Get the users who have accepted the current user as a friend
        accepted_friends_ids = FriendRequest.objects.filter(
            from_user=user, status=FriendRequest.Status.ACCEPTED
        ).values_list('to_user', flat=True)
        
        # Return the User objects corresponding to those IDs
        return User.objects.filter(id__in=accepted_friends_ids)

#To List the Pending request in user's list
    
class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        
    
        return FriendRequest.objects.filter(to_user=user, status=FriendRequest.Status.PENDING)



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def current_user(request):
    
#     user = UserSerializer(request.user, many=False)

#     return Response(user.data)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_user(request):

#     user = request.user
#     data = request.data

#     user.first_name = data['first_name']
#     user.last_name = data['last_name']
#     user.username = data['email']
#     user.email = data['email']

#     if data['password'] != "":
#         user.password = make_password(data['password'])


#     user.save()

#     serializer = UserSerializer(user, many=False)

#     return Response(serializer.data)