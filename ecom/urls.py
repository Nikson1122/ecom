from . import views

from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
      path('signup/', views.signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
]