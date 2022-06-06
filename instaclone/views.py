from django.shortcuts import render
from django.views.generic import ListView, DetailView

from instaclone.models import Post

# Create your views here.
# def index(request):
#     return render(request,'index.html', {})

class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    