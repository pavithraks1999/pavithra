from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.handle_signup, name='signup'),
    path('login', views.login, name="login"),
    path('handlelogin', views.handle_login, name='handle_login'),
    path('home', views.home, name="home"),
    path('logout/', views.logout_view, name='logout'),
]