biel-files-index
================

Creates an index of the biel-files resources for import to the BIEL
website.

Development
===========

All these commands require an environment variable `$IMAGE_LABEL` to be
set.

To build: `make build`

To run: `make run`

To run unit tests: `make test`. Also requires environment variable
`$HTMLCOV_DIR` to be set. If you're running in WSL1, this needs to be
reachable via your Docker share, e.g. `/c/Users/your_username/htmlcov`

To run linter: `make lint`

To open a shell in the container: `make shell`
