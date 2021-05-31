from django.urls import path
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    
    path('signup/', views.signupPage, name="signup"),
    path('signin/', views.signinPage, name="signin"),
    path('logout/', views.logoutUser, name="logout"),
    path('dashboard/', views.dashPage, name="dashboard"),
    path('index/', views.indexPage, name="index"),
    path('settings/', views.settingsPage, name="settings"),
    path('profile/', views.profilePage, name="profile"),
    path('create/', views.createPage, name="create"),
    path('find/', views.findPage, name="find"),
]

