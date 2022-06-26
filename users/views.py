from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework import filters
from users.models import MyUser

from users.serializers import  MyUserSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['email', 'username']

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]    
    