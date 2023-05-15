from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Channel, Community, CommunityComment



@admin.register(Channel)
class ChannelAdmin(ImportExportModelAdmin):
    list_display= [field.name for field in Channel._meta.fields]


@admin.register(Community)
class CommunityAdmin(ImportExportModelAdmin):
    list_display= [field.name for field in Community._meta.fields]

@admin.register(CommunityComment)
class CommunityCommentAdmin(ImportExportModelAdmin):
    list_display= [field.name for field in CommunityComment._meta.fields]


