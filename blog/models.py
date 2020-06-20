from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from django.utils.html import strip_tags
import markdown
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
    tags = models.ManyToManyField(Tag,blank=True,null=True,verbose_name='标签')
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})



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


