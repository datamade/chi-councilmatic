from django import template
from councilmatic.settings import ALDER_EXTRAS, CITY_VOCAB

register = template.Library()


@register.filter
def get_person_headshot(person):
    for p in ALDER_EXTRAS:
        if person:
            if person.slug.startswith(p):
                return f"/static/images/manual-headshots/{ALDER_EXTRAS[p]['image']}"

    return "/static/images/headshot_placeholder.png"


@register.filter
def get_legistar_link(object):
    for source in object.sources.all():
        return f"<a href='{source.url}' target='_blank' rel='nofollow'><i class='fa fa-fw fa-external-link'></i> View on the {CITY_VOCAB['SOURCE']} website</a>"  # noqa

    return ""


@register.filter
def get_mayor(year):
    if year == "2023":
        return "Brandon Johnson"
    if year == "2019":
        return "Lori Lightfoot"
    if year == "2015" or year == "2011":
        return "Rahm Emanuel"
    if year == "2007":
        return "Richard M. Daley"
    else:
        return ""
