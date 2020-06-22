from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from django.utils.html import strip_tags
import markdown
import re
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.utils.functional import cached_property

__all__ = ["Category",'Tag','Post']


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Post(models.Model):
    title = models.CharField('标题',max_length=50)
    body = models.TextField('正文')
    excerpt = models.CharField(max_length=200,blank=True,null=True,verbose_name='摘要')
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    edit_time = models.DateTimeField('修改时间',auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    views = models.PositiveIntegerField(default=0, editable=False)
    tags = models.ManyToManyField(Tag,blank=True,null=True,verbose_name='标签')
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    # cached_property提供缓存功能，它将被装饰方法调用返回的值缓存起来，下次访问时将直接读取缓存内容，而不需重复执行方法获取返回结果
    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def save(self,*args,**kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args,**kwargs)


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}
