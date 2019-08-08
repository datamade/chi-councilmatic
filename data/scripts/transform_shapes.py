import json
import sys

boundaries = json.load(sys.stdin)

for feature in boundaries['features']:
    division_id = 'ocd-division/country:us/state:il/place:chicago/ward:{}'.format(
        feature['properties']['ward']
    )
    feature['properties']['division_id'] = division_id

json.dump(boundaries, sys.stdout)
