from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm, EmailForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
import markdown

# Create your views here.

"""  # 可用类视图实现
def index(request):
    # return HttpResponse("欢迎来到 风雨兼程")
    "
    return render(request,'fengyujc_blog/index.html',context={
        'title': '风雨兼程',
        'welcome': '欢迎来到 风雨兼程'
    })
    "
    post_list = Post.objects.all().order_by('-created_time')  # - 表示逆序
    return render(request, 'fengyujc_blog/index.html', context={
        'post_list': post_list
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    # 对post的body的值做一下渲染,把Markdown文本转为HTML文本再传递给模板
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'fengyujc_blog/detail.html', context=context)


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'fengyujc_blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'fengyujc_blog/index.html', context={'post_list': post_list})
"""


# 类视图实现
class IndexView(ListView):
    model = Post
    template_name = 'fengyujc_blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):  # 在类视图中通过 get_context_data 传递模板变量字典
        context = super().get_context_data(**kwargs)  # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)  # 将分页导航条的模板变量更新到 context 中,ListView 使用这个字典中的模板变量去渲染模板

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 3]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[((page_number - 4) if (page_number - 4) > 0 else 0):page_number - 1]
            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[((page_number - 4) if (page_number - 4) > 0 else 0):page_number - 1]
            right = page_range[page_number:page_number + 3]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class CategoryView(ListView):  # 也可以直接继承 IndexView
    model = Post
    template_name = 'fengyujc_blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))  # URL 捕获的命名组参数值保存在实例的 kwargs 属性
        return super(CategoryView, self).get_queryset().filter(category=cate)  # 覆写父类方法,获取指定分类下的文章列表数据,而不是全部列表数据


class ArchivesView(ListView):
    model = Post
    template_name = 'fengyujc_blog/index.html'
    context_object_name = 'post_list'


class PostDetailView(DetailView):
    model = Post
    template_name = 'fengyujc_blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):  # 覆写 get 方法的目的是统计文章阅读量
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response  # 最终传递给浏览器的 HTTP 响应是 get 方法返回的 HttpResponse 对象

    def get_object(self, queryset=None):  # 覆写 get_object 方法的目的是对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)  # 'markdown.extensions.toc'
        ])
        post.body = md.convert(post.body)  # 给 post 实例动态添加了 md 属性
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):  # 覆写 get_context_data 的目的是将评论表单、post 下的评论列表传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class ContactView(ListView):
    model = Post
    template_name = 'fengyujc_blog/contact.html'

    def get_context_data(self, **kwargs):  # 覆写 get_context_data 的目的是将评论邮件表单传递给模板
        context = super(ContactView, self).get_context_data(**kwargs)
        form = EmailForm()
        context.update({
            'form': form,
        })
        return context


class FullwidthView(ListView):
    model = Post
    template_name = 'fengyujc_blog/full-width.html'
    context_object_name = 'post_list'


class AboutView(ListView):
    model = Post
    template_name = 'fengyujc_blog/about.html'


def search(request):
    q = request.GET.get('q')  # 通过表单 get 方法提交的数据保存在 request.GET
    error_msg = ''

    if not q:
        error_msg = '输入关键词'
        return render(request, 'fengyujc_blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    # icontains是查询表达式,在模型需要筛选的属性后面跟上两个下划线, Q对象用于包装查询表达式
    return render(request, 'fengyujc_blog/index.html', {'error_msg': error_msg,
                                                            'post_list': post_list})


