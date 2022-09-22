from django.contrib import admin
from backend.models import bookmarked_files, file_likes, file_upload, reported_file, searched_file, user_details, contact_us

admin.site.register(user_details)
admin.site.register(bookmarked_files)
admin.site.register(file_likes)
admin.site.register(file_upload)
admin.site.register(reported_file)
admin.site.register(searched_file)
admin.site.register(contact_us)
