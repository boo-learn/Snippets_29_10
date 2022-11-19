from django import template
register = template.Library()


def is_empty(value, alt):
   if value:
       return value
   return alt


register.filter('is_empty', is_empty)