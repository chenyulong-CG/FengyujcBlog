from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
import markdown
"""
django.contrib.auth 是Django内置的应用,
User是 Django已经写好的用户模型,
专门用于处理网站用户的注册、登录等流程
"""


# Create your models here.
# 一个python类对应一个数据库表格
class Category(models.Model):  # 分类
    """
        Django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        Django 还提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
        Django 内置的全部类型可查看文档：
        https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)


class Tag(models.Model):  # 标签
    name = models.CharField(max_length=100)


@python_2_unicode_compatible
class Post(models.Model):  # 文章
    def __str__(self):
        return self.title

    def get_absolute_url(self):  # 自定义 get_absolute_url 方法
        return reverse('fengyujc_blog:detail', kwargs={'pk': self.pk})  # 从django.urls中导入reverse函数

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):  # 复写 save 方法实现保存摘要
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:100] + '......'  # 去掉 HTML 文本里的 HTML 标签
        super(Post, self).save(*args, **kwargs)  # 调用父类的 save 方法将数据保存到数据库中

    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文使用 TextField
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本
    body = models.TextField()
    # 分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求必须存入数据，否则就会报错
    # 指定 CharField 的 blank=True 参数值后可以允许空值
    excerpt = models.CharField(max_length=200, blank=True)
    """
    把文章对应的数据库表和分类、标签对应的数据库表关联起来,关联形式稍有不同
    规定一篇文章只能对应一个分类,但是一个分类下可以有多篇文章,使用 ForeignKey,即一对多的关联关系
    文章和分类实际上是通过文章数据库表中分类ID这一列关联
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 级联删除
    """
    而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以使用 ManyToManyField，表明这是多对多的关联关系
    规定文章可以没有标签，因此为标签 tags 指定了 blank=True
    多对多的关系无法再像一对多的关系中的例子一样在文章数据库表加一列分类ID来关联,因此需要额外建一张表来记录文章和标签之间的关联
    https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    """
    tags = models.ManyToManyField(Tag, blank=True)
    # 通过 ForeignKey 把文章和 User 关联起来,一对多的关联关系,和 Category 类似
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:  # 这个内部类通过指定一些属性来规定这个类该有的一些特性,可以删掉视图函数中对文章列表中返回结果进行排序的代码
        ordering = ['-created_time', 'title']

    views = models.PositiveIntegerField(default=0)  # 该类型的值只允许为正整数或 0
