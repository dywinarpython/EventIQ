from django import template

register = template.Library()


@register.filter(name='return_one_error')
def return_one_error(value):
    if value:
        for errors in value.values():
            if errors:
                return errors[0]
    return ''
