.PHONY: build run test lint shell

build:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker build . -t biel-files:$(BF_IMAGE_LABEL)

run:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker run --rm biel-files:$(BF_IMAGE_LABEL) > biel-files.json

test:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	test -n "$(BF_HTMLCOV_DIR)" # $$BF_HTMLCOV_DIR
	docker build . -t biel-files:$(BF_IMAGE_LABEL)
	docker run -it --rm \
		--entrypoint=/app/test.sh \
		--volume $(BF_HTMLCOV_DIR):/app/htmlcov \
		biel-files:$(BF_IMAGE_LABEL)

lint:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker build . -t biel-files:$(BF_IMAGE_LABEL)
	docker run -it --rm \
		--entrypoint=/app/lint.sh \
		biel-files:$(BF_IMAGE_LABEL)

shell:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker run -it --rm \
		--entrypoint=/bin/bash \
		biel-files:$(BF_IMAGE_LABEL)
