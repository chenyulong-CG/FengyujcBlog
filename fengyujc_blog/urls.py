from django.conf.urls import url
from . import views


app_name = 'fengyujc_blog'
urlpatterns = [  # 点击链接，就跳转到相关url
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
#    url(r'^search/$', views.search, name='search'),  # 简单搜索
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^fullwidth/$', views.FullwidthView.as_view(), name='fullwidth'),
    url(r'^about/$', views.AboutView.as_view(), name='about')
]

