from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('vote/<str:slug>/', views.detail, name = 'detail'),
    path('result/<str:slug>/', views.result, name = 'result'),
    path('result/', views.result, name = 'result'),
    path('signup/', views.signup, name = 'signup'),
    path('signin', views.signin, name = 'signin'),
    path('logout/', views.logoutView, name = 'logout'),
]