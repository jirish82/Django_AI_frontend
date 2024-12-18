from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('conversation/', views.conversation_view, name='conversation'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/conversation/', views.conversation_api, name='conversation_api'),
]