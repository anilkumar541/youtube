from django.urls import path
from . import views


app_name="coreapp"

urlpatterns = [
    path("", views.homePage, name="homepage"),
    path("video_details/<int:pk>/", views.videoDetails, name="video_details"), #get video 

    # comment feature endpoints
    path("comment/", views.ajax_save_comment, name="comment"), #save comment
    path("delete_comment/", views.ajax_delete_comment, name="delete_comment"), #delete_comment

    #add new subscriber
    path("add_subscriber/<int:pk>/", views.add_new_subscribers, name="add_subscriber"), #add new subscriber
    path("load_channel_subscribers/<int:pk>/", views.load_channel_subscribers, name="load_channel_subscribers"), #load channel subscriber

    # likes feature endpoints
    path("like/<int:pk>/",views.add_new_likes, name="add-new_likes"),
    path("load_likes/<int:pk>/",views.load_video_likes, name="load_video_likes"),

    #get featured video
    path("featured_video/", views.get_featured_video, name="featured_video"),

    # save_video_profile
    path("save_video/<int:video_id>/", views.save_video, name="save_video"),

    # search videos
    path("search_video/", views.searchView, name="search_video"),

    # tags_url
    path("tags/<slug:tag_slug>/", views.tag_list, name="tags")



]
