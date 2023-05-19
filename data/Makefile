.PHONY: all clean
.INTERMEDIATE: intermediate/*

all: final/chicago_shapes.geojson
clean:
	rm -Rf final/chicago_shapes.geojson

final/chicago_shapes.geojson: intermediate/chicago_shapes.geojson
	cat $< | python3 scripts/transform_shapes.py > $@

intermediate/chicago_shapes.geojson: raw/chicago_shapes_raw.geojson
	ogr2ogr -simplify 0.0001 -f GeoJSON -nlt MULTIPOLYGON $@ $<

raw/chicago_shapes_raw.geojson:
	curl "https://data.cityofchicago.org/api/geospatial/p293-wvbd?accessType=DOWNLOAD&method=export&format=GeoJSON" > $@
