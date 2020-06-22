from django import template
from blog.models import Post,Category,Tag
from django.db.models import Count
register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html')
def show_recent_post(num=5):
    return {'recent_post_list':Post.objects.all().order_by('-create_time')[:num]}


@register.inclusion_tag('blog/inclusions/_archives.html')
def show_archives():
    return {'date_list':Post.objects.dates('create_time','month', order='DESC')}


@register.inclusion_tag('blog/inclusions/_categories.html')
def show_category():
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {'category_list': category_list}


@register.inclusion_tag('blog/inclusions/_tags.html')
def show_tag():
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    print(tag_list)
    return {'tag_list': tag_list}
