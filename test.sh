#!/usr/bin/env bash
coverage run --branch --source . --omit "test_*" -m unittest discover
coverage report
coverage html
