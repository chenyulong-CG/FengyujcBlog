from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    title = 'Networking风雨兼程'
    link = '/'
    description = 'Networking风雨兼程的博客文章'

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
