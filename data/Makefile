.PHONY: all clean
all: final/shapes/chicago_shapes.json
clean:
	rm -Rf final/shapes/chicago_shapes.json

final/shapes/chicago_shapes.json:
	mkdir -p $(dir $@)
	python3 scripts/extract_shapes.py > $@
