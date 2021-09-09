from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    template = 'posts/index.html'

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)

    post_list = Post.objects.filter(group=group)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    profile = get_object_or_404(User, username=username)

    post_list = Post.objects.filter(author=profile)
    post_count = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
        'post_count': post_count
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    profile = get_object_or_404(User, username=post.author)
    posts_count = Post.objects.filter(author=profile).count()

    context = {
        'post': post,
        'posts_count': posts_count,
        'profile': profile
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)

    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('posts:post_detail', post_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            update_post = form.save(commit=False)
            post.text = update_post.text
            post.group = update_post.group
            post.save()
            return redirect('posts:post_detail', post_id)
    is_edit = True
    form = PostForm(instance=post)
    context = {
        'is_edit': is_edit,
        'form': form,
        'post_id': post_id
    }
    return render(request, template, context)
