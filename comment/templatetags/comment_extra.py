from django import template
from ..forms import CommentForm


register = template.Library()


@register.inclusion_tag('comment/inclusions/_form.html')
def show_comment_form(post,form=None):
    if form is None:
        form = CommentForm()

    return {
        'form': form,
        'post': post
    }


@register.inclusion_tag('comment/inclusions/_list.html')
def show_comments(post):
    comment_list = post.comment_set.all().order_by('-create_time')
    comment_list_count = comment_list.count()
    return {
        'comment_list':comment_list,
        'comment_list_count':comment_list_count,
    }
