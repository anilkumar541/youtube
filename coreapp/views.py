from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from coreapp.models import Video, Comment
from channel_app.models import Channel
from userauthentication_app.models import Profile
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from taggit.models import Tag

def homePage(request):
    video=Video.objects.filter(visibility="Public")
    context={
        "video":video
    }
    return render(request, "home_page.html", context)


def videoDetails(request, pk):

    video=Video.objects.get(id=pk)
    channel= Channel.objects.get(user= video.user)
    channel.total_views += 1
    channel.save()

    video.views +=1
    video.save()


    # # suggesting video
    video_tags_id = video.tags.values_list("id", flat=True)
    similar_videos = Video.objects.filter(tags__id__in=video_tags_id).exclude(id=pk)
    similar_videos = similar_videos.annotate(same_tags=Count("tags")).order_by("-same_tags", "-date")[:25]

    # getting all comment related to a video
    comment= Comment.objects.filter(active=True, video=video).order_by("-date")


    context={
        "video":video,
        "channel":channel,
        "comment":comment,
        "similar_videos": similar_videos
    }
    return render(request, "video.html", context)


# save video
def save_video(request, video_id):
    video= Video.objects.get(id=video_id)
    user= request.user.profile
    # user= Profile.objects.get(user=request.user)
    print("hit hua")

    if video in user.saved_videos.all():
        user.saved_videos.remove(video)
    else:
        user.saved_videos.add(video)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))




# save comment
def ajax_save_comment(request):
    if request.method == "POST":
        id=request.POST.get("id")
        comment=request.POST.get("comment")

        video=Video.objects.get(id=id)
        user= request.user
        new_comment= Comment.objects.create(comment=comment, user=user, video=video)
        print(new_comment, "jsdnjnjn")
        new_comment.save()

        response= "Comment posted"
        return HttpResponse(response)

    return HttpResponse("get method")



# delete comment
@csrf_exempt
def ajax_delete_comment(request):
    if request.method== "POST":
        id=request.POST.get("id")
        comment=Comment.objects.get(id=id)
        comment.delete()
        return JsonResponse({"status": 1})
    return JsonResponse({"status": 2})



# add_new_subscribers
@csrf_exempt
def add_new_subscribers(request, pk):
    if pk == 4:
        pk = 3
        
    channel_id= Channel.objects.get(id=pk)
    user= request.user
    if user in channel_id.subscribers.all():
        # If user is subscribed, unsubscribe them
        channel_id.subscribers.remove(user)
        response = "Subscribe"
    else:
        # If user is not subscribed, subscribe them
        channel_id.subscribers.add(user)
        response = "Unsubscribe"

    # return JsonResponse(response, safe=False)
    return HttpResponse(f"{response}")


    
# load channel subscribers
def load_channel_subscribers(request, pk):

    if pk == 4:
        pk = 3
    print("channel", pk)
    channel_data= Channel.objects.get(id=pk)
    print("channel", channel_data)
    subs=channel_data.subscribers.count()
    return HttpResponse(f"{subs}")




# add_new_likes
@csrf_exempt
def add_new_likes(request, pk):
    video= Video.objects.get(id=int(pk))
    user= request.user
    print(video, user, "lsmdlmfls")

    if user in video.likes.all():
        video.likes.remove(user)
        # video.subscribers(user)
        
        like_response = "Like"
    else:
        video.likes.add(user)
        like_response = "Dislike"

    return JsonResponse(like_response, safe=False)



    
# load video likes
def load_video_likes(request, pk):
    video= Video.objects.get(id=pk)
    likes_list= list(video.likes.values())
    return JsonResponse(likes_list, safe=False)



# get featured video
def get_featured_video(request):
    featured_video= Video.objects.get(featured=True)
    return render(request, "channel_profile_copy.html", {"featured_video":featured_video})




def searchView(request):
    video=Video.objects.filter(visibility="Public").order_by("-date")
    query= request.GET.get("q")

    if query:
        video= video.filter(
            Q(title__icontains=query)|Q(description__icontains=query)
        ).distinct()

    context={
        "video":video,
        "query": query
    }
    return render(request, "search.html", context)


def tag_list(request, tag_slug=None):
    video=Video.objects.filter(visibility="Public").order_by("-date")
    tag=None
    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        video= video.filter(tags__in =[tag])

    context={
        "video":video,
        "tag": tag
    }
    return render(request, "tags.html", context)
