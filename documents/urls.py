from django.urls import path
from . import views

urlpatterns = [
    path('tempfiles/<str:file_name>/', views.download_file, name='download_file'),
]
