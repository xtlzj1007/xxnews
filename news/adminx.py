#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import xadmin
from news.models import *
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 后台管理系统的标题
    site_title = "后台管理系统"
    # 底部显示信息
    site_footer = "底部信息"
    # 折叠样式
    menu_style = "accordion"


class TypeAdmin(object):
    # 在admin中显⽰顺序
    list_display = ["id", "name"]
    # 给admin添加搜索功能
    search_fields = ["id", "name"]
    # 筛选字段
    list_filter = ["id", "name"]
    # 排序字段
    ordering = ["id"]


class ContentAdmin(object):
    # 在admin中显⽰顺序
    list_display = ["id", "title", "picture", "image"]
    # 给admin添加搜索功能
    search_fields = ["id", "publish_time", "title", "picture"]
    # 排序字段
    ordering = ["-publish_time"]
    # 设置分页 每页显示数据的条数
    list_per_page = 20


class CommentAdmin(object):
    # 在admin中显⽰顺序
    list_display = ["id", "content", "user_id", "news_id", "state"]
    # 给admin添加搜索功能
    search_fields = ["id", "publish_time", "user_id", "news_id"]
    # 直接编辑字段
    list_editable = ["state"]
    # 排序字段
    ordering = ["-publish_time"]


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Type, TypeAdmin)
xadmin.site.register(Content, ContentAdmin)
xadmin.site.register(Comment, CommentAdmin)
