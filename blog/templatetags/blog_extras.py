from django import template
from blog.models import Post,Category,Tag
register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html')
def show_recent_post(num=5):
    return {'recent_post_list':Post.objects.all().order_by('-create_time')[:num]}


@register.inclusion_tag('blog/inclusions/_archives.html')
def show_archives():
    return {'date_list':Post.objects.dates('create_time','month', order='DESC')}


@register.inclusion_tag('blog/inclusions/_categories.html')
def show_category():
    return {'category_list': Category.objects.all()}


@register.inclusion_tag('blog/inclusions/_tags.html')
def show_tag():
    return {'tag_list': Tag.objects.all()}
