import json
import sys

import requests

BOUNDARY_SET = ['chicago-wards-2015']
BASE_URL = 'https://ocd.datamade.us'

session = requests.Session()


def get_response(url, params=None, timeout=60, **kwargs):
    """
    The OCD API has intermittently thrown 502 and 504 errors, so only proceed
    when receiving an 'ok' status.
    """
    response = session.get(url, params=params, timeout=timeout, **kwargs)

    if response.ok:
        return response
    else:
        message = '{url} returned a bad response - {status}'.format(
            url=url,
            status=response.status_code
        )
        raise requests.exceptions.HTTPError('ERROR: {0}'.format(message))


if __name__ == '__main__':
    """
    Extract shapes for each OCD Division entity from the OCD API.
    """
    shapes = {
        'type': 'FeatureCollection',
        'features': [],
    }
    for boundary in BOUNDARY_SET:
        bndry_set_url = BASE_URL + '/boundaries/' + boundary

        page_res = get_response(bndry_set_url + '/?limit=0')
        page_json = json.loads(page_res.text)

        for bndry_json in page_json['objects']:
            shape_url = BASE_URL + bndry_json['url'] + 'shape'
            shape_res = get_response(shape_url)
            shapes['features'].append({
                'type': 'Feature',
                'geometry': json.loads(shape_res.text),
                'properties': {
                    'division_id': bndry_json['external_id'],
                },
            })

    json.dump(shapes, sys.stdout)
