"""teammatefinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings

import account.views as account
import blog.views as blog

#app_name = 'blog'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog.index, name="home"),

    path('new/', blog.new, name="new"),
    path('create/', blog.create, name="create"),

    path('edit/<int:blog_id>', blog.edit, name="edit"),
    path('update/<int:blog_id>/<blog_slug>', blog.update, name="update"),
    path('delete/<int:blog_id>/<blog_slug>', blog.delete, name="delete"),

    path('search', blog.search, name='search'),


    path('mypage', account.mypage, name="mypage"),
    path('mypageBookmark', account.mypageBookmark, name="mypageBookmark"),
    path('bookmark', blog.bookmark, name="bookmark"),




    path('<int:blog_id>/<blog_slug>/comment', blog.add_comment_to_post,
         name="add_comment_to_post"),
    path('<int:blog_id>/<blog_slug>/', blog.detail, name="detail"),


    # 특정과목(카테고리)글만리스트
    path('<slug:category_slug>/', blog.blog_in_category, name='blog_in_category'),



    path('account/login', account.login_view, name="login"),
    path('account/logout', account.logout_view, name="logout"),
    path('account/register', account.register_view, name="register"),



]
