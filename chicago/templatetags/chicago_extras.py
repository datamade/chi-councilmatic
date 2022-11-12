from django import template
from councilmatic.settings import MANUAL_HEADSHOTS

register = template.Library()


@register.filter
def get_person_headshot(person):
    for p in MANUAL_HEADSHOTS:
        if person.slug.startswith(p):
            return f"/static/images/manual-headshots/{MANUAL_HEADSHOTS[p]['image']}"

    return "/static/images/headshot_placeholder.png"
