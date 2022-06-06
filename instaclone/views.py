from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
# def index(request):
#     return render(request,'index.html', {})

class HomeView(ListView):
    model = Post
    template_name = 'index.html'

class AtricleDetailView(DeprecationWarning):
    model = Post
    template_name = 'artcle_details.html'
