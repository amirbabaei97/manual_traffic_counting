from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter(name='arrow_image')
def arrow_image(stream):
    # Maps stream number to image file
    return static(f'images/arrow_{stream}.png')

@register.filter(name='image_position')
def image_position(stream):
    # Assigns CSS classes based on stream number for image positioning
    if stream in [1, 2, 3]:
        return 'image-left'
    elif stream in [4, 5, 6]:
        return 'image-bottom'
    elif stream in [7, 8, 9]:
        return 'image-right'
    elif stream in [10, 11, 12]:
        return 'image-top'
    return ''  # Default case, no special positioning

