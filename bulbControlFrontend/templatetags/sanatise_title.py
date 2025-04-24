from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter(name="sanatise_title")
@stringfilter
def sanatise_title(s):
    s = s.replace(" ", "_")
    s = s.replace(",", "_")
    return s
