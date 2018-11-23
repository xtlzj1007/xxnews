"""news_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
# from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView
from news.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^admin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r"^$", IndexView.as_view()),
    url(r"^login", LoginView.as_view()),
    url(r"^logout", LogoutView.as_view()),
    url(r'^captcha/', include('captcha.urls')),
    url(r"^signup", SignupView.as_view()),
    url(r"^news/(?P<content_id>\d+)", NewsView.as_view()),
    url(r"^password_reset/(?P<user_id>\d+)$", password_reset),
    url(r"^setuser/(?P<user_id>\d+)", SetUserView.as_view()),
    url(r"^forgetpwd$", ForGetPassword.as_view()),
    url(r"^getpwd/(?P<user_id>\d+)/(?P<code>\w+)", getpwd),
    url(r"^type", TypeView.as_view()),
    url(r"^comment", CommentView.as_view()),
    url(r"^userinfo", UserInfoView.as_view()),
    url(r"^content", ContentView.as_view())
]
