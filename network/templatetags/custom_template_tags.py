from django import template
register = template.Library()


@register.simple_tag
def to_list(a, args):

    if args.filter(follow=a).exists():
        exists = True
    else:
        exists = False
    return exists