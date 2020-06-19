.PHONY: build clean run run-all test lint edit shell

build:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker build . -t biel-files:$(BF_IMAGE_LABEL)

clean:
	rm -f biel-files*.json

run:
	test -n "$(BF_IMAGE_LABEL)"   # $$BF_IMAGE_LABEL
	test -n "$(BF_REPO_USERNAME)" # $$BF_REPO_USERNAME
	test -n "$(BF_REPO_ID)"       # $$BF_REPO_ID
	test -n "$(BF_BRANCH_ID)"     # $$BF_BRANCH_ID
	test -n "$(BF_LANGUAGE_CODE)" # $$BF_LANGUAGE_CODE
	test -n "$(BF_DIR_NAME)"      # $$BF_DIR_NAME
	test -n "$(BF_DIR_LABEL)"     # $$BF_DIR_LABEL
	docker run --rm \
		--env BF_GITHUB_USERNAME=$(BF_GITHUB_USERNAME) \
		--env BF_GITHUB_PASSWORD=$(BF_GITHUB_PASSWORD) \
		--env BF_REPO_USERNAME=$(BF_REPO_USERNAME) \
		--env BF_REPO_ID=$(BF_REPO_ID) \
		--env BF_BRANCH_ID=$(BF_BRANCH_ID) \
		--env BF_LANGUAGE_CODE=$(BF_LANGUAGE_CODE) \
		--env BF_DIR_NAME="$(BF_DIR_NAME)" \
		--env BF_DIR_LABEL="$(BF_DIR_LABEL)" \
		biel-files:$(BF_IMAGE_LABEL) > biel-files.json

run-all:
	test -n "$(BF_IMAGE_LABEL)"   # $$BF_IMAGE_LABEL
	test -n "$(BF_REPO_USERNAME)" # $$BF_REPO_USERNAME
	test -n "$(BF_REPO_ID)"       # $$BF_REPO_ID
	test -n "$(BF_BRANCH_ID)"     # $$BF_BRANCH_ID
	rm -f biel-files*.json
	# English
	docker run --rm \
		--env BF_GITHUB_USERNAME=$(BF_GITHUB_USERNAME) \
		--env BF_GITHUB_PASSWORD=$(BF_GITHUB_PASSWORD) \
		--env BF_REPO_USERNAME=$(BF_REPO_USERNAME) \
		--env BF_REPO_ID=$(BF_REPO_ID) \
		--env BF_BRANCH_ID=$(BF_BRANCH_ID) \
		--env BF_LANGUAGE_CODE="en" \
		--env BF_DIR_NAME="review-guide" \
		--env BF_DIR_LABEL="Reviewers' Guide" \
		biel-files:$(BF_IMAGE_LABEL) > biel-files-en.json
	# French
	docker run --rm \
		--env BF_GITHUB_USERNAME=$(BF_GITHUB_USERNAME) \
		--env BF_GITHUB_PASSWORD=$(BF_GITHUB_PASSWORD) \
		--env BF_REPO_USERNAME=$(BF_REPO_USERNAME) \
		--env BF_REPO_ID=$(BF_REPO_ID) \
		--env BF_BRANCH_ID=$(BF_BRANCH_ID) \
		--env BF_LANGUAGE_CODE="fr" \
		--env BF_DIR_NAME="guide-d'examen" \
		--env BF_DIR_LABEL="Guide des Examinateurs" \
		biel-files:$(BF_IMAGE_LABEL) > biel-files-fr.json
	# Combine
	jq -s add biel-files*.json > biel-files.json

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
		--env BF_PYLINT_PARAMS=$(BF_PYLINT_PARAMS) \
		--entrypoint=/app/lint.sh \
		biel-files:$(BF_IMAGE_LABEL)

edit:
	$(EDITOR) README.md makefile Dockerfile *.sh *.py

shell:
	test -n "$(BF_IMAGE_LABEL)" # $$BF_IMAGE_LABEL
	docker run -it --rm \
		--entrypoint=/bin/bash \
		biel-files:$(BF_IMAGE_LABEL)
