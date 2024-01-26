"""
URL configuration for movielibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from mainpage import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add-movie-to-ranking/<int:movie_id>/', views.add_movie_to_ranking, name='add_movie_to_ranking'),
    path('user-ranking/', views.user_ranking, name='user_ranking'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('my_account/', views.my_account, name='my_account'),
    path('logout/', views.logout_user, name='logout'),
    path('my_account/edit', views.edit_profile, name='edit_profile'),
    path('my_account/delete_account', views.delete_account, name='delete_account'),
    path('remove_movie/<int:position>/', views.remove_movie, name='remove_movie'),
]
