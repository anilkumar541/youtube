from django.urls import path
from . import views



app_name="channel_app"

urlpatterns = [
    path("subsciber_count/", views.get_channel_subscriber, name="subscriber_count"),
    path("channel_profile/<int:pk>/", views.get_channel_profile, name="channel_profile"),
    path("get_channel_videos/<int:pk>/", views.get_channel_videos, name="get_channel_videos"),
    path("channel_about/<int:pk>/", views.channel_about, name="channel_about"),
    path("channel_community/<int:pk>/", views.channel_community, name="channel_community"),
    path("channel_community_detail/<int:channel_pk>/<int:community_pk>/", views.channel_community_detail, name="channel_community_detail"),
    path("create_community_comment/<int:community_pk>/", views.create_community_comment, name="create_community_comment"),
    path("delete_community_comment/<int:community_id>/<int:comment_id>/", views.delete_community_comment, name="delete_community_comment"),
    path("like_community_post/<int:community_id>", views.like_community_post, name="like_community_post"),

    # upload video
    path("video_upload/", views.video_upload, name="video_upload"),
    # edit video
    path("edit_upload/<int:channel_id>/<int:video_id>/", views.video_edit, name="edit_upload"),


    # community post create url
    path("create_community_post/<int:channel_id>/", views.create_community_post, name="create_community_post"),
    path("edit_community_post/<int:channel_id>/<int:community_post_id>/", views.edit_community_post, name="edit_community_post"),
    path("delete_community_post/<int:channel_id>/<int:community_post_id>/", views.delete_community_post, name="delete_community_post"),

    # whatsapp
    path('share-via-whatsapp/<str:text>/', views.share_via_whatsapp, name='share_via_whatsapp'),

]