from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Post, Follow, Comment
from django.contrib.auth.models import User 
from .forms import PostForm, EditForm, CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
# def index(request):
#     return render(request,'index.html', {})

class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    ordering = ['-post_date']

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request, 'categories.html', {'cats':cats.title(),'category_posts':category_posts })

def LikeView(request,pk):
    post =  get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    # fields = '__all__'
    # fields = ('title', 'body')

class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'
    # fields = ('title', 'body')

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

    def user_profile(request, username):
        user_prof = get_object_or_404(User, username=username)
        if request.user == user_prof:
            return redirect('profile', username=request.user.username)
        user_posts = user_prof.profile.posts.all()
        followers = Follow.objects.filter(followed=user_prof.profile)
        follow_status = None
        for follower in followers:
            if request.user.profile == follower.follower:
                follow_status = True
            else:
                follow_status = False
        params = {
            'user_prof': user_prof,
            'user_posts': user_posts,
            'followers': followers,
            'follow_status': follow_status
        }
        print(followers)
        return render(request, 'registration/user_profile.html', params)


    @login_required(login_url='login')
    def post_comment(request, id):
        image = get_object_or_404(Post, pk=id)
        is_liked = False
        if image.likes.filter(id=request.user.id).exists():
            is_liked = True
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                savecomment = form.save(commit=False)
                savecomment.post = image
                savecomment.user = request.user.profile
                savecomment.save()
                return HttpResponseRedirect(request.path_info)
        else:
            form = CommentForm()
        params = {
            'image': image,
            'form': form,
            'is_liked': is_liked,
            'total_likes': image.total_likes()
        }
        return render(request, 'instagram/single_post.html', params)

