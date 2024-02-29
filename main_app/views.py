import uuid
import boto3
import os
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from .models import *
from rest_framework import status, permissions, viewsets, parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.shortcuts import render, redirect, get_object_or_404
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import Concat
from django.db.models import F
from django.db.models.functions import ExtractDay, ExtractMonth
from django.db.models import Q

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        username = self.kwargs['username']
        return get_object_or_404(User, username=username)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.AllowAny]

class WishViewSet(viewsets.ModelViewSet):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        id = self.kwargs.get('id')
        username = self.kwargs.get('username')
        if (id):
            print(id)
            person = get_object_or_404(Person, id=id)
            # Filter Wish objects based on the user's ID
            queryset = Wish.objects.filter(person=person)
            return queryset
        elif (username):
            print(username)
            user = get_object_or_404(User, username=username)
            # Filter Wish objects based on the user's ID
            queryset = Wish.objects.filter(user=user, person=None)
            return queryset
        
    def post(self, request, id):
        # Check if 'person' is present in the request data
        if 'person' in request.data:
            print("Wish is for a person")
            person_id = request.data['person']
            person = Person.objects.get(id=person_id)
            wish_serializer = WishSerializer(data=request.data)
            if wish_serializer.is_valid():
                # If the wish is for a person, save it with the associated person
                wish = wish_serializer.save(person=person)
                serialized_wish = WishSerializer(wish)
                return Response(serialized_wish.data, status=status.HTTP_201_CREATED)
            else:
                return Response(wish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If 'person' is not present in the request data, associate the wish with a user
            user = User.objects.get(id=id)
            wish_serializer = WishSerializer(data=request.data)
            if wish_serializer.is_valid():
                # If the wish is not for a person, save it with the associated user
                wish = wish_serializer.save(user=user)
                serialized_wish = WishSerializer(wish)
                return Response(serialized_wish.data, status=status.HTTP_201_CREATED)
            else:
                return Response(wish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

            

    
    # def post(self, request, id):
    #     user = User.objects.get(id=id)
    #     wish_serializer = WishSerializer(data=request.data)
    #     if wish_serializer.is_valid():
    #         wish = wish_serializer.save(user=user)
            
    #         serialized_wish = WishSerializer(wish)
    #         return Response(serialized_wish.data, status=status.HTTP_201_CREATED)
    #     return Response(wish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request, id):
    #     user = User.objects.get(id=id)
    #     wish = WishSerializer(data=request.data)
    #     if wish.is_valid():
    #         wish.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    
class WishDetailView(viewsets.ModelViewSet):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        id = self.kwargs['id']
        # return get_object_or_404(Person, id=id)
        return Wish.objects.get(pk=id)
    
    def delete(self, request, *args, **kwargs):
        wish = self.get_object()
        wish.delete()
        return Response(status=204)
    
    def put(self, request, *args, **kwargs):
        wish = self.get_object()
        serializer = self.get_serializer(wish, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        created_by = get_object_or_404(User, username=username)
        # Filter Person objects based on the user
        queryset = Person.objects.filter(created_by=created_by)
        queryset = queryset.order_by('-birthday')
        return queryset
    
    def post(self, request, id):
            user = User.objects.get(id=id)
            person_serializer = PersonSerializer(data=request.data)
            if person_serializer.is_valid():
                person = person_serializer.save(created_by=user)
                # Serialize the created person instance
                serialized_person = PersonSerializer(person)
                return Response(serialized_person.data, status=status.HTTP_201_CREATED)
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonDetailView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        id = self.kwargs['id']
        # return get_object_or_404(Person, id=id)
        return Person.objects.get(pk=id)
    
    def put(self, request, *args, **kwargs):
        person = self.get_object()
        serializer = self.get_serializer(person, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        person = self.get_object()
        person.delete()
        return Response(status=204)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return get_object_or_404(UserProfile, user=user)
    
    def post(self, request):
        print (request)
        user = User.objects.get(username=request.data.get("username"))
        user_profile = UserProfileSerializer(data={'user': user.id})
        if user_profile.is_valid():
            user_profile.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LogoutView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# class SignupView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         try:
#             new_user = User.objects.create(username=username, email=email)
#             new_user.set_password(password)
#             new_user.save()
#             return Response(status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def add_photo(request, id):
    user_profile = UserProfile.objects.get(id=id)

    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print (photo_file)
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo.objects.create(url=url)
            photo.save()
            user_profile.image = photo
            user_profile.save()

        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            return JsonResponse(data = {}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data = {}, status=status.HTTP_201_CREATED)

@csrf_exempt
def add_photo_person(request, id):
    person = Person.objects.get(id=id)

    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print (photo_file)
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo.objects.create(url=url)
            photo.save()
            
            person.image = photo
            person.save()
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            return JsonResponse(data = {}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data = {}, status=status.HTTP_201_CREATED)
    
@csrf_exempt
def add_photo_wish(request, id):
    wish = Wish.objects.get(id=id)

    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print (photo_file)
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo.objects.create(url=url)
            photo.save()
            
            wish.images.add(photo)
            wish.save()
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            return JsonResponse(data = {}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data = {}, status=status.HTTP_201_CREATED)
    
@csrf_exempt
def delete_photo(request, id):
    # Retrieve the photo object by its ID
    photo = Photo.objects.get(id=id)

    try:
        # Delete the photo object
        photo.delete()
        return JsonResponse(data={}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print('An error occurred while deleting the photo:', e)
        return JsonResponse(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)