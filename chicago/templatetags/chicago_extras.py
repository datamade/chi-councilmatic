from django import template
from councilmatic.settings import ALDER_EXTRAS, CITY_VOCAB

register = template.Library()


@register.filter
def get_person_headshot(person):
    for p in ALDER_EXTRAS:
        if person.slug.startswith(p):
            return f"/static/images/manual-headshots/{ALDER_EXTRAS[p]['image']}"

    return "/static/images/headshot_placeholder.png"


@register.filter
def get_legistar_link(object):
    for source in object.sources.all():
        if source.note == "web":
            return f"<a href='{source.url}' target='_blank' rel='nofollow'><i class='fa fa-fw fa-external-link'></i> View on the {CITY_VOCAB['SOURCE']} website</a>"  # noqa
