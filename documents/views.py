from django.http import HttpResponse, Http404
import os
from django.utils.encoding import smart_str
from django.conf import settings

# Allows users to download a specific file from a predetermined directory on the server. It includes error handling for non-existent files and sets appropriate headers to facilitate the download in web browsers.
def download_file(request, file_name):
    full_path = os.path.join(settings.BASE_DIR, "documents", "tempfiles", file_name)

    if not os.path.exists(full_path):
        raise Http404("File not found")

    with open(full_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{smart_str(file_name)}"'
        return response
