
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blog.models import *
from blog.views import bookmark

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('home')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


# 마이페이지
@login_required
def mypage(request):
    logged_in_user = request.user
    logged_in_user_blogs = Blog.objects.filter(author=request.user)

    return render(request, 'mypage.html', {'blogs': logged_in_user_blogs})


def mypageBookmark(request):
    logged_in_user = request.user
    logged_in_user_comment = Comment.objects.get(author_name=request.user)
    return render(request, 'mypageBookmark.html', {'comments': logged_in_user_comment})
