from django.shortcuts import render, get_object_or_404, redirect
from fengyujc_blog.models import Post
from .models import Comment
from .forms import CommentForm, EmailForm

# Create your views here.


def post_comment(request, post_pk):
    # 获取被评论的文章，后面需要把评论和被评论的文章关联起来
    post = get_object_or_404(Post, pk=post_pk)
    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求
    # 只有当用户的请求为 post 时才需要处理表单数据
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象
        # 利用这些数据构造 CommentForm 的实例，就生成了 Django 的表单
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # 利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
            comment.post = post  # 将评论和被评论的文章关联起来
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()  # 调用 xxx_set 属性获取一个类似于 objects 的模型管理器
            context = {
                'post': post,
                "form": form,
                "comment_list": comment_list
            }
            return render(request, 'fengyujc_blog/detail.html', context=context)
    return redirect(post)


def post_email(request):
    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求
    # 只有当用户的请求为 post 时才需要处理表单数据
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象
        # 利用这些数据构造 EmailForm 的实例，就生成了 Django 的表单
        form = EmailForm(request.POST)
        print(form)
        if form.is_valid():
            email = form.save(commit=False)  # 利用表单的数据生成 Email 模型类的实例，但还不保存评论数据到数据库
            email.save()
            print('test')
            print(email)
            return 'fengyujc_blog:contact'
        else:

            context = {
                "form": form,
            }
            return render(request, 'fengyujc_blog/contact.html', context=context)
    return 'fengyujc_blog:contact'