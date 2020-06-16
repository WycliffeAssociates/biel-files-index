.PHONY: run test

run:
	test -n "$(IMAGE_LABEL)" # $$IMAGE_LABEL
	docker build . -t biel-files:$(IMAGE_LABEL)
	docker run --rm biel-files:$(IMAGE_LABEL) > biel-files.json

test:
	test -n "$(IMAGE_LABEL)" # $$IMAGE_LABEL
	docker build . -t biel-files:$(IMAGE_LABEL)
	docker run -it --rm \
		--entrypoint=/app/test_main.py \
		biel-files:$(IMAGE_LABEL)
