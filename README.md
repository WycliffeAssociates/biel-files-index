biel-files-index
================

Creates an index of the biel-files resources for import to the BIEL
website.

Development
===========

All these commands require an environment variable `$BF_IMAGE_LABEL` to be
set, which is the label for the Docker image to use, e.g. "prod" or "dev"

To build: `make build`

To run: `make run`

To run unit tests: `make test`

To run linter: `make lint`

To open a shell in the container: `make shell`

Most of these commands require one or more environment variables to be set.
The `env-example.sh` file can be sourced to set up some sensible defaults.
