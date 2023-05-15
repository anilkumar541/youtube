from django.shortcuts import render,HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from channel_app.models import Channel, Community, CommunityComment
from coreapp.models import Video
from django.db.models import Count
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import VideoForm, CommunityForm
import urllib.parse


def share_via_whatsapp(request, text):
    # Encode the text for use in the WhatsApp link
    encoded_text = urllib.parse.quote(text)

    # Construct the WhatsApp link
    url = f'https://api.whatsapp.com/send?text={encoded_text}'

    # Redirect the user to the WhatsApp link
    return redirect(url)


# write code here to get channel subscribers with given channel id
def get_channel_subscriber(request, pk=2):
    print("got hit")
    channel_subs_count=Channel.objects.get(id=pk).subscribers.count()

    if channel_subs_count <= 9:
        return HttpResponse(f"{channel_subs_count} Subscriber")
    return HttpResponse(f"{channel_subs_count} Subscribers")

    # return JsonResponse(response, safe=False)
    


# get channel profile data
def get_channel_profile(request, pk):
    channel = get_object_or_404(Channel, id=pk)
    
    # getting channel featured video if there is
   
    try:
        featured_video= get_object_or_404(Video, user=channel.user.id, featured= True)
    except Exception as obj:
        featured_video=None
        # messages.warning(request, "Only one video can featured ")

    # get popular videos
    popular_videos=Video.objects.filter(user= channel.user, visibility= "Public").order_by("-views")

    context={
        "popular_videos": popular_videos,
        "channel": channel,
        "featured_video": featured_video
    }


    return render(request, "channel_profile_copy.html", context)


# Get a specific channel's all video
def get_channel_videos(request, pk):
    channel = get_object_or_404(Channel, id=pk)
    videos=Video.objects.filter(user= channel.user, visibility= "Public").order_by("-date")

    context={
        "videos": videos,
        "channel": channel
    }
    return render(request, "channel_videos.html", context)


def channel_about(request, pk):
    channel = get_object_or_404(Channel, id=pk)
    

    context={
        
        "channel": channel
    }
    return render(request, "channel_about.html", context)



# get all the community post of a specific channel
def channel_community(request, pk):
    channel = get_object_or_404(Channel, id=pk)
    community = Community.objects.filter(channel=channel, status="Active").order_by("-date")
    
    context={
        "channel": channel,
        "community": community
    }

    return render(request, "channel_community.html", context)


# channel community detail
def channel_community_detail(request, channel_pk, community_pk):
    channel = get_object_or_404(Channel, id=channel_pk)
    community = Community.objects.get(id= community_pk ,channel=channel, status="Active")
    # listing all comments for a community post
    comments= CommunityComment.objects.filter(active=True, community=community).order_by("-date")

    context={
        "channel": channel,
        "community": community,
        "comments": comments
    }

    return render(request, "channel_community_detail.html", context)

@login_required
def create_community_comment(request, community_pk):
    if request.method == "POST":
        community = Community.objects.get(id= community_pk, status="Active")
        comment= request.POST.get("comment")
        user= request.user

        create_comment= CommunityComment.objects.create(community=community, comment=comment, user=user)
        create_comment.save()
        channel_pk = community.channel.pk
        print("i m here")
        messages.success(request, "Comment posted")
        return redirect(reverse('channel_app:channel_community_detail', args=[channel_pk, community_pk]))
        
    # # messages.warning(request, "Comment not posted")
    return render(request, "channel_community_detail.html")



# delete community comment 
@login_required
def delete_community_comment(request, community_id, comment_id):
    community= Community.objects.get(id=community_id)
    comment= CommunityComment.objects.get(id=comment_id, community=community)
    comment.delete()
    messages.success(request, "Comment deleted successfully")

    # return redirect(reverse('channel_app:channel_community_detail', args=[channel_pk, community_pk]))

    # return redirect("channel_community_detail", community.channel.id, comment_id)
    return redirect(reverse('channel_app:channel_community_detail', args=[community.channel.id, community_id]))



# like community_post
def like_community_post(request, community_id):
    community= Community.objects.get(id=community_id)
    user= request.user

    if user in community.likes.all():
        community.likes.remove(user)
    else:
        community.likes.add(user)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    



# upload video
@login_required
def video_upload(request):
    user= request.user
    if request.method=="POST":
        form=VideoForm(request.POST, request.FILES)
        if form.is_valid():
            new_form= form.save(commit=False)
            new_form.user=user
            form.save()
            form.save_m2m()
            messages.success(request, f"Video uploaded successfully")
            return redirect("channel_app:channel_profile", user.channel.id)
    else:
        form=VideoForm
        # print(form.title)
        context={
            "form": form
        }
        return render(request, "video_upload.html", context)
    
# edit uploaded video
@login_required
def video_edit(request, channel_id, video_id):
    video= Video.objects.get(id=video_id)
    channel= Channel.objects.get(id=channel_id)
    user= request.user
    if request.method=="POST":
        form=VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            new_form= form.save(commit=False)
            new_form.user=user
            form.save()
            form.save_m2m()
            messages.success(request, f"Video Edited successfully")
            return redirect("channel_app:channel_profile", user.channel.id)
    else:
        form=VideoForm(instance=video)
        # print(form.title)
        context={
            "form": form
        }
        return render(request, "video_upload.html", context)




@login_required
def create_community_post(request, channel_id):
    channel= Channel.objects.get(id=channel_id)
    user=request.user

    if request.method == "POST":
        form= CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            new_form= form.save(commit=False)
            new_form.channel= channel
            new_form.save()
            post_id= new_form.id
            messages.success(request, "Community post created")
            return redirect("channel_app:channel_community_detail", channel.id, post_id)

    else:
        form= CommunityForm()
        context={
            "form": form
        }
        return render(request, "community-create.html", context)



@login_required
def edit_community_post(request, channel_id, community_post_id):
    channel= Channel.objects.get(id=channel_id)
    post=Community.objects.get(id=community_post_id)
    user=request.user

    if request.method == "POST":
        form= CommunityForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_form= form.save(commit=False)
            new_form.channel= channel
            new_form.save()
            post_id= new_form.id
            messages.success(request, "Community post edited")
            return redirect("channel_app:channel_community_detail", channel.id, post_id)

    else:
        form= CommunityForm(instance=post)
        context={
            "form": form
        }
        return render(request, "community-create.html", context)



@login_required
def delete_community_post(request, channel_id, community_post_id):
    channel= Channel.objects.get(id=channel_id)
    post=Community.objects.get(id=community_post_id)
    user=request.user

    post.delete()
    return redirect("channel_app:channel_community", channel.id)