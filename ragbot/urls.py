from .admin import admin_site
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin_site.urls),
    path('documents/', include('documents.urls')),
    path('', include('conversations.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
