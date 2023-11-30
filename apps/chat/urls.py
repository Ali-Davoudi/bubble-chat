from django.urls import path

from . import views

urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name='create-room'),
    path('chat-admin', views.chat_admin, name='chat_admin'),
    path('chat-admin/add-user/', views.add_user, name='add_user'),
    path('chat-admin/user/<uuid:uuid>/edit/', views.edit_user, name='edit_user'),
    path('chat-admin/user/<uuid:uuid>/', views.user_detail, name='user_detail'),
    path('chat-admin/<str:uuid>/', views.room, name='room'),
    path('chat-admin/<str:uuid>/delete/', views.delete_room, name='delete_room'),
]
