from django import template
register = template.Library()


@register.simple_tag
def to_list(a, args):
    """ Custom template tag to determine if a 
        user is following another for button colour change """
    if args.filter(follow=a).exists():
        exists = True
    else:
        exists = False
    return exists


@register.simple_tag
def post_liker(a, args):
    """ Custom template tag to determine if 
        a user likes a post or not """
    if args.likes.filter(user=a).exists():
        exists = True
    else:
        exists = False
    return exists