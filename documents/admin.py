from django.contrib import admin
from services.singleton import weaviate_service


@admin.action(description='Delete selected documents')
def delete_selected(modeladmin, request, queryset):
    uuids = list(queryset.values_list('chunks_ids', flat=True).exclude(chunks_ids__isnull=True))
    uuids = [item for sublist in uuids for item in sublist]
    if uuids:
        weaviate_service.delete_documents(uuids=uuids)
    queryset.delete()


class DocumentAdmin(admin.ModelAdmin):
    fields = ('title', 'file', 'description')
    list_display = ('title', "file", 'created_at', 'updated_at')

    actions = [delete_selected]
