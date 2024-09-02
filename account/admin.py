from django.contrib import admin
from . models import FriendRequest

# Register your models here.
@admin.register(FriendRequest)
class FriendRequestadmin(admin.ModelAdmin):
    list_display=['id','from_user','to_user','status']