from django.contrib import admin
from documents.admin import DocumentAdmin
from django.contrib.auth.admin import UserAdmin
from documents.models import Document, MyUser

# Sets up a custom Django admin interface. Registers two models MyUser and Document to be managed through this custom admin interface
# Allows  for greater flexibility in customizing the Django admin interface, such as adding custom views, changing the look and feel, or modifying the behavior of the admin site
class MyAdminSite(admin.AdminSite):
    ...

admin_site = MyAdminSite(name='myadmin')
admin_site.register(MyUser, UserAdmin)
admin_site.register(Document, DocumentAdmin)
