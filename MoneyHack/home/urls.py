from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('expenses/', include("expenses.urls")),
    path('analytics/', include("analytics.urls")),
    path('goals/', include("goals.urls")),
    path('chatbot/', include("chatbot.urls")),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]