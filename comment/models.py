from django.db import models
from blog.models import Post
# Create your models here.


class Comment(models.Model):
    name = models.CharField('名字',max_length=20)
    email = models.EmailField('邮箱')
    url = models.URLField('网址',blank=True,null=True)
    text = models.TextField('内容')
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    post = models.ForeignKey(Post,verbose_name='文章',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f"{self.name}:{self.text[:20]}"



