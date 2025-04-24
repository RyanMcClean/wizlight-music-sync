"""Custom tags for Django templates"""

from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter(name="sanatise_title")
@stringfilter
def sanatise_title(s):
    """Used to remove whitespace and special characters from a string in a Django template"""
    s = s.replace(" ", "_")
    s = s.replace(",", "_")
    return s
