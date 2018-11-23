import random
import json
import hashlib
import news.zhenzismsclient as smsclient
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse
from django.views import View
from news.forms import SignupForm, CommentForm, ForGetPasswordForm, UserInfoForm, PasswordForm
from news.models import UserInfo, Content, Comment, Type
from rest_framework import generics
from news.serializers import TypeSerializer, CommentSerializer, ContentSerializer, UserInfoSerializer


class TypeView(generics.ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CommentView(generics.ListAPIView):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer


class UserInfoView(generics.ListAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class ContentView(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


def send_dx(mobile):
    yzm = str(random.randint(1000, 9999))
    api_url = "http://sms_developer.zhenzikj.com"
    app_id = 100097  # id
    app_secret = "NTI3ZjUyN2EtYjc2Yi00N2FiLTgwYjMtOGQ5MzE2NjJhN2Uz"  # 随机密码
    client = smsclient.ZhenziSmsClient(api_url, app_id, app_secret)
    result = client.send(mobile, "您的验证码是%s" % yzm)
    return json.loads(result), yzm


def hash_code(code):
    m = hashlib.md5()
    m.update(code.encode('utf-8'))
    return m.hexdigest()


class IndexView(View):
    def get(self, request):
        # add_content()
        types = Type.objects.all()
        search = request.GET.get("search", None)
        type_id = request.GET.get("type_id", None)

        if type_id:
            type_id = int(type_id)
            news_list_all = Content.objects.filter(type_id=type_id)
        elif search:
            news_list_all = Content.objects.filter(title__iregex="\w*%s\w*" % search)
        else:
            news_list_all = Content.objects.all().order_by("id")
            # 所有文章最热排行
        hot_news = Content.objects.all().order_by("-clicked")[:10]
        # 　24小时最热排行
        # 获取今日的时间
        # today = datetime.now() # 当前时间
        # 计算出要分类的时间
        # yesterday = today - timedelta(days=3) # 当前时间－24
        ##print(yesterday)__lte <=   __gte >=    24 ()
        # hot_news = Content.objects.filter(publish_time__lte=today, publish_time__gte=yesterday).order_by("-clicked")[:10]

        # 格式化字符串
        return render(request, 'index.html', locals())


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": "用户名或密码有误！"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # 保存注册信息到数据库
            # 我们自己加密
            pwd = make_password(request.POST.get("password"))
            # 使用自定义的方法保存用户信息
            UserInfo.objects.create(
                password=pwd,
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                mobile=request.POST.get("mobile"),
                gender=request.POST.get("gender")
            )
            # 注册成功跳转到登录页面
            return redirect("/login")
        else:
            return render(request, "signup.html", {"form": form})


class NewsView(View):
    def get(self, request, content_id):
        types = Type.objects.all()
        data = Content.objects.get(id=content_id)
        data.clicked = int(data.clicked) + 1
        data.save()
        form = CommentForm()
        comment_list = Comment.objects.filter(news_id=data, restore=None)
        hot_news = Content.objects.all().order_by("-clicked")[:10]
        return render(request, "news.html", locals())

    def post(self, request, content_id):
        form = CommentForm(request.POST)
        ip = request.META['REMOTE_ADDR']
        if form.is_valid():
            if request.user.id:
                restore = request.POST.get("restore", None)
                if restore:
                    Comment.objects.create(
                        user_id=request.user,
                        news_id=Content.objects.get(id=content_id),
                        content=request.POST.get("content"),
                        restore=Comment.objects.get(id=request.POST.get("restore")),
                        restore_user=UserInfo.objects.get(id=request.POST.get("restore_user")),
                        ip=ip,
                    )
                else:
                    Comment.objects.create(
                        user_id=request.user,
                        news_id=Content.objects.get(id=content_id),
                        content=request.POST.get("content"),
                        ip=ip,
                    )
            else:
                return HttpResponse("登陆后才能评论！")
        return redirect("/news/%s" % content_id)


class SetUserView(View):
    def get(self, request, user_id):
        types = Type.objects.all()
        user = UserInfo.objects.get(id=user_id)
        return render(request, "setuser.html", locals())

    def post(self, request, user_id):
        types = Type.objects.all()
        user = UserInfo.objects.get(id=user_id)
        form = UserInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/")
        return render(request, "setuser.html", locals())


@login_required(login_url="/login")
def password_reset(request, user_id):
    if request.method == "GET":
        return render(request, "password_reset.html", locals())
    elif request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            pwd1 = request.POST.get("password")
            pwd2 = request.POST.get("re_password")
            if pwd1 == pwd2:
                user = UserInfo.objects.get(id=user_id)
                user.password = make_password(pwd1)
                user.save()
                return redirect("/login")
    return render(request, "password_reset.html", locals())


class ForGetPassword(View):
    def get(self, request):
        form = ForGetPasswordForm()
        return render(request, "forgetpwd.html", locals())

    def post(self, request):
        form = ForGetPasswordForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            user = UserInfo.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user:
                result, yzm = send_dx(user.mobile)  # 找到用户手机号，给用户发送短信
                print(result, yzm)
                if result.get("code") == 0:  # 结果的返回码为0,发送短信成功
                    return redirect('/getpwd/%s/%s' % (user.id, hash_code(yzm)))
        return render(request, "forgetpwd.html", locals())


def getpwd(request, user_id, code):
    if request.method == "GET":
        return render(request, "getpwd.html", locals())

    elif request.method == "POST":
        new_code = request.POST.get("new_code")
        user = UserInfo.objects.get(id=user_id)
        if user and code == hash_code(new_code):
            login(request, user)
            return redirect("/password_reset/%s" % user_id)
        else:
            return render(request, "getpwd.html", locals())
