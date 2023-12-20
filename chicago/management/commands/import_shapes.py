import json

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import GEOSGeometry

from councilmatic_core import models


class Command(BaseCommand):
    help = "Import boundary shapefiles for Post entities"

    def add_arguments(self, parser):
        parser.add_argument(
            "geojson_file",
            help=(
                "The location of the GeoJSON file containing shapes for each "
                "Division, relative to the project root. The file should be "
                "formatted as a GeoJSON FeatureCollection where each Feature A) "
                "corresponds to a distinct Division and B) has a 'division_id' "
                "attribute in the 'properties' object. "
            ),
        )

    def handle(self, *args, **options):
        self.stdout.write("Populating shapes for Posts...")
        shapes_populated = 0

        with open(options["geojson_file"]) as shapef:
            shapes = json.load(shapef)

        features = self._get_or_raise(
            shapes, "features", 'Could not find the "features" array in the input file.'
        )

        for feature in features:
            shape = self._get_or_raise(
                feature, "geometry", 'Could not find a "geometry" key in the Feature.'
            )
            properties = self._get_or_raise(
                feature,
                "properties",
                'Could not find a "properties" key in the Feature.',
            )
            division_id = self._get_or_raise(
                properties,
                "division_id",
                'Could not find a "division_id" key in the Feature properties.',
            )

            models.Post.objects.filter(division_id=division_id).update(
                shape=GEOSGeometry(json.dumps(shape))
            )
            shapes_populated += 1

        self.stdout.write(
            self.style.SUCCESS("Populated {} shapes".format(str(shapes_populated)))
        )

    def _get_or_raise(self, dct, key, msg):
        """
        Check to see if 'dct' has a key corresponding to 'key', and raise an
        error if it doesn't.
        """
        format_prompt = (
            "Is the input file formatted as a GeoJSON FeatureCollection "
            'where each feature has a "division_id" property?'
        )
        if not dct.get(key):
            raise CommandError(msg + " " + format_prompt)
        else:
            return dct[key]
