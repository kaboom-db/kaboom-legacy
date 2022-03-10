from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from comics.models import Comic
from cartoons.models import Cartoon
from users.models import WatchedEpisode, ReadIssue, UserData, CartoonSubscription, ComicSubscription
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from users.models import get_user_image
from social.models import Thought

import base64
import requests

# Create your views here.
def index(request):
    num_of_comics = Comic.objects.count()
    num_of_cartoons = Cartoon.objects.count()
    num_of_users = User.objects.count()
    num_of_thoughts = Thought.objects.count()
    return render(request, 'website/index.html', context={'num_of_comics': num_of_comics, 'num_of_cartoons': num_of_cartoons, 'num_of_users': num_of_users, 'num_of_thoughts': num_of_thoughts})

def docs(request):
    return HttpResponseRedirect('https://kaboom-db.github.io/kaboom-docs/')

def tocs(request):
    return HttpResponseRedirect('https://github.com/kaboom-db/kaboom-api/blob/master/LICENSE#L71-L621')

def privacy(request):
    return HttpResponseRedirect('https://github.com/kaboom-db/kaboom-api/blob/master/PRIVACY.md')

def dev_guides(request):
    return HttpResponseRedirect('https://github.com/kaboom-db/kaboom-api/blob/master/DEV_GUIDELINES.md')

def v1(request):
    return render(request, 'website/v1.html')

def profile(request):
    context = {}
    if not request.user.is_anonymous:
        user_data = UserData.objects.get(user=request.user)
        user_cartoons = CartoonSubscription.objects.filter(user=request.user)
        user_comics = ComicSubscription.objects.filter(user=request.user)
        context = { 'image': get_user_image(request.user.email), 'user_data': user_data, 'user_cartoons': user_cartoons, 'user_comics': user_comics }
    return render(request, 'website/profile.html', context = context)

def watched(request, username):
    context = {}
    # user = User.objects.filter(username=username).first()
    userdata = UserData.objects.filter(user__username=username, private=False).first()
    if userdata:
        user = userdata.user
        last = WatchedEpisode.objects.filter(user=user).order_by('-watched_at').first()
        if last:
            episode_nr = 'S' + str(last.episode.season_number) + 'E' + str(last.episode.episode_number)
            if last.episode.screenshot:
                last_watched_image = 'data:image/png;base64,' + base64.b64encode(requests.get(last.episode.screenshot).content).decode('utf-8')
            else:
                last_watched_image = ''
            context = {'exists': True, 'last_watched_title': last.episode.name, 'last_watched_image': last_watched_image, 'episode_nr': episode_nr, 'username': username}
        else:
            context = {'exists': True, 'last_watched_title': 'Nothing watched yet', 'last_watched_image': '', 'episode_nr': '', 'username': username}
        
        return render(request, 'website/watched.html', context = context, content_type="image/svg+xml")
    else:
        context = {'exists': False}
        return render(request, 'website/watched.html', context = context)

def read(request, username):
    context = {}
    userdata = UserData.objects.filter(user__username=username, private=False).first()
    if userdata:
        user = userdata.user
        last = ReadIssue.objects.filter(user=user).order_by('-read_at').first()
        if last:
            issue_nr = '#' + str(last.issue.issue_number_absolute) 
            if last.issue.cover_image:
                last_read_image = 'data:image/png;base64,' + base64.b64encode(requests.get(last.issue.cover_image).content).decode('utf-8')
            else:
                last_read_image = ''
            context = {'exists': True, 'last_read_title': str(last.issue.series), 'last_read_image': last_read_image, 'issue_nr': issue_nr, 'username': username}
        else:
            context = {'exists': True, 'last_read_title': 'Nothing read yet', 'last_read_image': '', 'issue_nr': '', 'username': username}
        
        return render(request, 'website/read.html', context = context, content_type="image/svg+xml")
    else:
        context = {'exists': False}
        return render(request, 'website/read.html', context = context)

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'