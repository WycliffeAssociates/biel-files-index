# Some sensible defaults for running, testing, linting
# usage: source source-dev-env.sh

# Required: Which image to build and use
export BF_IMAGE_LABEL=local-dev

# Required for run
export BF_REPO_USERNAME=wa-biel
export BF_REPO_ID=biel-files
export BF_BRANCH_ID=master

# Required for test
export BF_HTMLCOV_DIR=/tmp/htmlcov

# Required for lint
export BF_PYLINT_PARAMS=--output-format=colorized
