from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from comics.models import Comic
from cartoons.models import Cartoon
from users.models import Thought, WatchedEpisode
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from users.models import get_user_image

# Create your views here.
def index(request):
    num_of_comics = Comic.objects.count()
    num_of_cartoons = Cartoon.objects.count()
    num_of_users = User.objects.count()
    num_of_thoughts = Thought.objects.count()
    return render(request, 'website/index.html', context={'num_of_comics': num_of_comics, 'num_of_cartoons': num_of_cartoons, 'num_of_users': num_of_users, 'num_of_thoughts': num_of_thoughts})

def docs(request):
    return HttpResponseRedirect('https://kaboom.readthedocs.io/en/latest/')

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
        context = { 'image': get_user_image(request.user.email) }
    return render(request, 'website/profile.html', context = context)

def watched(request, username):
    context = {}
    user = User.objects.filter(username=username).first()
    if user:
        last = WatchedEpisode.objects.filter(user=user).order_by('-watched_at').first()
        if last:
            episode_nr = 'S' + str(last.episode.season_number) + 'E' + str(last.episode.episode_number)
            context = {'exists': True, 'last_watched_title': last.episode.name, 'last_watched_image': last.episode.screenshot, 'episode_nr': episode_nr, 'username': username}
        else:
            context = {'exists': True, 'last_watched_title': 'Nothing watched yet', 'last_watched_image': '', 'episode_nr': '', 'username': username}
    else:
        context = {'exists': False}

    return render(request, 'website/watched.html', context = context)

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'