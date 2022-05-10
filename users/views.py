from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework import filters
from users.models import MyUser

from users.serializers import  MyUserSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    permissions_class = permissions.IsAuthenticated
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['email', 'username']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return MyUser.objects.all()
        else:
            return MyUser.objects.filter(id=user.id)        