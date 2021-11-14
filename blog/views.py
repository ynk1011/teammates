from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from .models import *
from .forms import BlogForm, CommentForm
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST


from urllib.parse import urlparse
# Create your views here.


def index(request):
    blog = Blog.objects
    return render(request, 'index.html', {'blogs': blog})


def home(request):
    blog = Blog.objects
    return render(request, 'home.html', {'blogs': blog})


@login_required
def create(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.pub_date = timezone.now()
        new_blog.author = request.user

        new_blog.save()
        hashtags = request.POST['hashtags']
        hashtag = hashtags.split(",")
        for tag in hashtag:
            ht = HashTag.objects.get_or_create(hashtag_name=tag)
            new_blog.hashtag.add(ht[0])

        return redirect('detail', new_blog.id, new_blog.slug)
    return redirect('home')


# 해당 과목의 모든 글 보여주기
def blog_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    blogs = Blog.objects.all()
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        blogs = blogs.filter(category=current_category)

    return render(request, 'list.html', {'categories': categories, 'current_category': current_category, 'blogs': blogs})


def detail(request, blog_id, blog_slug=None):
    blog_detail = get_object_or_404(Blog, id=blog_id, slug=blog_slug)
    blog_hashtag = blog_detail.hashtag.all()
    bookmark = blog_detail.bookmark.all()

    return render(request, 'detail.html', {'blog': blog_detail, 'hashtags': blog_hashtag, 'bookmarks': bookmark})


def new(request):
    form = BlogForm()
    return render(request, 'new.html', {'form': form})


def edit(request,  blog_id, blog_slug=None):
    blog_detail = get_object_or_404(Blog, pk=blog_id, slug=blog_slug)
    return render(request, 'edit.html', {'blog': blog_detail})


def update(request, blog_id, blog_slug=None):
    blog_update = get_object_or_404(Blog, pk=blog_id, slug=blog_slug)
    blog_update.title = request.POST['title']
    blog_update.body = request.POST['body']
    blog_update.save()
    return redirect('home')


def delete(request, blog_id, blog_slug=None):
    blog_delete = get_object_or_404(Blog, pk=blog_id, slug=blog_slug)
    blog_delete.delete()
    return redirect('home')


def add_comment_to_post(request, blog_id, blog_slug=None):
    blog = get_object_or_404(Blog, pk=blog_id, slug=blog_slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.save()
            return redirect('detail', blog_id, blog_slug)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


# 검색
def search(request):
    blogs = Blog.objects.all().order_by('-id')

    q = request.POST.get('q', "")

    if q:
        blogs = blogs.filter(body__icontains=q)
        return render(request, 'search.html', {'blogs': blogs, 'q': q})

    else:
        return render(request, 'search.html')


# 저장
@login_required
def bookmark(request):
    if request.is_ajax():
        blog_id = request.GET['blog_id']
        blog = Blog.objects.get(id=blog_id)

        user = request.user
        if blog.bookmark.filter(id=user.id).exists():
            blog.bookmark.remove(user)
            message = "북마크 취소"
        else:
            blog.bookmark.add(user)
            message = "북마크"
        context = {"message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')
