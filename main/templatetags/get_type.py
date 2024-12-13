from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def get_type(context):
    name = context['request']
    req = name.GET
    return req['name'] if 'name' in req else ''