.PHONY: build clean run test lint edit shell

build:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker build . -t biel-files:$(BF_IMAGE_LABEL)

clean:
	rm -f biel-files.json

run:
	test -n "$(BF_IMAGE_LABEL)"   # $$BF_IMAGE_LABEL
	test -n "$(BF_REPO_USERNAME)" # $$BF_REPO_USERNAME
	test -n "$(BF_REPO_ID)"       # $$BF_REPO_ID
	test -n "$(BF_BRANCH_ID)"     # $$BF_BRANCH_ID
	docker run --rm \
		--env BF_GITHUB_USERNAME=$(BF_GITHUB_USERNAME) \
		--env BF_GITHUB_PASSWORD=$(BF_GITHUB_PASSWORD) \
		--env BF_REPO_USERNAME=$(BF_REPO_USERNAME) \
		--env BF_REPO_ID=$(BF_REPO_ID) \
		--env BF_BRANCH_ID=$(BF_BRANCH_ID) \
		biel-files:$(BF_IMAGE_LABEL) > biel-files.json

test:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	test -n "$(BF_HTMLCOV_DIR)" # $$BF_HTMLCOV_DIR
	docker run -it --rm \
		--entrypoint=/app/test.sh \
		--volume $(BF_HTMLCOV_DIR):/app/htmlcov \
		biel-files:$(BF_IMAGE_LABEL)

lint:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker run -it --rm \
		--env BF_PYLINT_PARAMS=$(BF_PYLINT_PARAMS) \
		--entrypoint=/app/lint.sh \
		biel-files:$(BF_IMAGE_LABEL)

edit:
	$(EDITOR) README.md makefile Dockerfile *.sh *.py *.json

shell:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker run -it --rm \
		--entrypoint=/bin/bash \
		biel-files:$(BF_IMAGE_LABEL)
