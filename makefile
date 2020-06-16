.PHONY: build run test lint shell

build:
	test -n "$(IMAGE_LABEL)" # $$IMAGE_LABEL
	docker build . -t biel-files:$(IMAGE_LABEL)

run:
	test -n "$(IMAGE_LABEL)" # $$IMAGE_LABEL
	docker run --rm biel-files:$(IMAGE_LABEL) > biel-files.json

test:
	test -n "$(IMAGE_LABEL)" # $$IMAGE_LABEL
	test -n "$(HTMLCOV_DIR)" # $$HTMLCOV_DIR
	docker build . -t biel-files:$(IMAGE_LABEL)
	docker run -it --rm \
		--entrypoint=/app/test.sh \
		--volume $(HTMLCOV_DIR):/app/htmlcov \
		biel-files:$(IMAGE_LABEL)

lint:
	test -n "$(IMAGE_LABEL)" # $$IMAGE_LABEL
	docker build . -t biel-files:$(IMAGE_LABEL)
	docker run -it --rm \
		--entrypoint=/app/lint.sh \
		biel-files:$(IMAGE_LABEL)

shell:
	test -n "$(IMAGE_LABEL)" # $$IMAGE_LABEL
	docker run -it --rm \
		--entrypoint=/bin/bash \
		biel-files:$(IMAGE_LABEL)
