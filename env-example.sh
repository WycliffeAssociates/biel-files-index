# Some sensible defaults for running, testing, linting
# usage: source source-dev-env.sh

# Required: Which image to build and use
export BF_IMAGE_LABEL=local-dev

# Required for run-all
export BF_REPO_USERNAME=wa-biel
export BF_REPO_ID=biel-files
export BF_BRANCH_ID=master

# Required for run
export BF_LANGUAGE_CODE=en
export BF_DIR_NAME=review-guide
export BF_DIR_LABEL="Reviewers' Guide"

# Required for test
export BF_HTMLCOV_DIR=/tmp/htmlcov

# Required for lint
export BF_PYLINT_PARAMS=--output-format=colorized
