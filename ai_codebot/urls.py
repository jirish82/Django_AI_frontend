from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.login_view, name='codebot_login'),
    path('conversation/', views.conversation_view, name='codebot_conversation'),
    path('logout/', auth_views.LogoutView.as_view(next_page='codebot_login'), name='codebot_logout'),
    path('api/conversation/', views.conversation_api, name='codebot_conversation_api'),
]