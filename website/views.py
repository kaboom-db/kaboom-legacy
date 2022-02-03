from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from comics.models import Comic
from cartoons.models import Cartoon
from users.models import Thought
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic

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
    return HttpResponseRedirect('https://github.com/kaboom-db/kaboom-api/blob/master/LICENSE')

def privacy(request):
    return HttpResponseRedirect('https://github.com/kaboom-db/kaboom-api/blob/master/PRIVACY.md')

def dev_guides(request):
    return HttpResponseRedirect('https://github.com/kaboom-db/kaboom-api/blob/master/DEV_GUIDELINES.md')

def v1(request):
    return render(request, 'website/v1.html')

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'