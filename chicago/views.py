from django.shortcuts import render
from datetime import date, timedelta
from chicago.models import ChicagoBill
from councilmatic_core.models import Event

def index(request):
    
    recently_passed = []
    # go back in time at 10-day intervals til you find 3 passed bills
    for i in range(0,-100, -10):
        begin = date.today() + timedelta(days=i)
        end = date.today() + timedelta(days=i-10)

        leg_in_range = ChicagoBill.objects\
                             .exclude(last_action_date=None)\
                             .filter(last_action_date__lte=begin)\
                             .filter(last_action_date__gt=end)\
                             .order_by('-last_action_date')
        passed_in_range = [l for l in leg_in_range \
                           if l.inferred_status == 'Passed']

        recently_passed.extend(passed_in_range)
        if len(recently_passed) >= 3:
            recently_passed = recently_passed[:3]
            break

    context = {
        'recently_passed': recently_passed,
        'next_council_meeting': Event.next_city_council_meeting(),
        'upcoming_committee_meetings': list(Event.upcoming_committee_meetings()),
    }

    return render(request, 'chicago/index.html', context)
