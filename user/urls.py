from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
]
