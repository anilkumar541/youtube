from django.contrib import admin
from .models import Video, Comment
from import_export.admin import ImportExportModelAdmin


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    list_display= [field.name for field in Video._meta.fields]

@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display= [field.name for field in Comment._meta.fields]


    


