BOUNDARIES_SOURCE := "https://data.cityofchicago.org/api/geospatial/sp34-6z76?method=export&format=GeoJSON"

.PHONY: all clean
all: final/shapes/chicago_shapes.json
clean:
	rm -Rf final/shapes/chicago_shapes.json

raw/shapes/chicago_shapes.json:
	curl $(BOUNDARIES_SOURCE) > $@

final/shapes/chicago_shapes.json: raw/shapes/chicago_shapes.json
	cat $< | python3 scripts/transform_shapes.py > $@
