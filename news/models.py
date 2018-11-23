from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="新闻类型")

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "新闻类型"
        verbose_name_plural = verbose_name
        db_table = "news_type"


class UserInfo(AbstractUser):
    gender = models.CharField(max_length=1, choices=(("0", "男"), ("1", "女")), verbose_name="性别", default="0")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    image = models.ImageField(upload_to="image/%Y/%m", default='default.png', max_length=30, verbose_name="头像")

    def __str__(self):
        return "%s" % self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = "user_info"


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(to="UserInfo", to_field="id", related_name="context", verbose_name="用户")
    type_id = models.ForeignKey(to="Type", to_field="id", related_name="context", verbose_name="新闻类型")
    title = models.CharField(max_length=100, verbose_name="标题")
    picture = models.CharField(max_length=20, verbose_name="标签")
    content = RichTextUploadingField(verbose_name="新闻内容")
    image = models.ImageField(upload_to="image/%Y/%m", default='default.png', max_length=255, verbose_name="图片")
    publish_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    clicked = models.IntegerField(verbose_name="点击量", default=0)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = "文章内容"
        verbose_name_plural = verbose_name
        db_table = "content"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(to="UserInfo", to_field="id", verbose_name="用户")
    news_id = models.ForeignKey(to="Content", to_field="id", verbose_name="新闻")
    content = RichTextUploadingField(verbose_name="评论内容")
    publish_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")
    state = models.BooleanField(default=True, verbose_name="审核状态")
    ip = models.GenericIPAddressField(verbose_name="用户IP地址")
    # 4.5 回复:评论　评论
    restore = models.ForeignKey(to="self", to_field="id", related_name="re_comment", verbose_name="回复对象", null=True,
                                blank=True)
    restore_user = models.ForeignKey(to="UserInfo", to_field="id", related_name="restore", verbose_name="回复的用户",
                                     null=True, blank=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = "评论内容"
        verbose_name_plural = verbose_name
        db_table = "comment"
