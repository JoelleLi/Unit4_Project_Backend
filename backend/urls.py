"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView
from main_app.views import RegisterView, UserDetailView, UserProfileView, PersonDetailView, WishDetailView
from main_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'photos', views.PhotoViewSet)
router.register(r'wishes', views.WishViewSet)
router.register(r'people', views.PersonViewSet)
router.register(r'userprofiles', views.UserProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name ='auth_logout'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    # path('register/', views.SignupView.as_view(), name='auth_register'),
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user-detail'),
    path('userprofile/', views.UserProfileView.as_view(), name='user-profiles'),
    path('userprofile/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('userprofiles/', views.UserProfileView.as_view(), name='add_user_profile'),
    path('userprofile/<int:id>/add_photo/', views.add_photo, name='add_photo_user'),
    path('persons/<str:username>/', views.PersonViewSet.as_view({'get': 'list'}), name='persons_list'),
    path('persons/profile/<int:id>/', views.PersonDetailView.as_view(), name='person_detail'),
    path('wishlist/<str:username>/', views.WishViewSet.as_view({'get': 'list'}), name='wishlist'),
    path('wishlist/wish/<int:id>/', views.WishDetailView.as_view({'get': 'retrieve'}), name='wish_detail'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
