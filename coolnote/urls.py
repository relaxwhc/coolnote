"""coolnote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from note import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH
    path('signup/', views.signup_user, name='signup_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # NOTE
    path('', views.home, name='home'),
    path('current/', views.current_note, name='current_note'),
    path('completed/', views.completed_note, name='completed_note'),
    path('create/', views.create_note, name='create_note'),
    path('note/<int:note_pk>', views.view_note, name='view_note'),
    path('note/<int:note_pk>/complete>', views.complete_note, name='complete_note'),
    path('note/<int:note_pk>/delete>', views.delete_note, name='delete_note'),
    ]
