from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('conversation/<uuid:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('new/', views.new_conversation, name='new_conversation'),
]
