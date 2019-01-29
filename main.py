#!/usr/bin/env python3
import argparse

import github

def main():
    args = parse_arguments()
    github_api = login_to_github(args.user, args.password)
    repo = github_api.get_repo("wa-biel/biel-files")
    tree = repo.get_git_tree("master",recursive=True)

def login_to_github(username, password):
    if (username == "" and password == ""):
        github_api = github.Github()
    else:
        github_api = github.Github(username, password)
    return github_api

def parse_arguments(): # pragma: no cover
    """ Configures and parses command-line arguments """

    argparser = argparse.ArgumentParser(
        description="Create index for biel-files GitHub repo")

    argparser.add_argument("--user",
                           nargs="?",
                           default="",
                           help="GitHub user, default anonymous")

    argparser.add_argument("--password",
                           nargs="?",
                           default="",
                           help="GitHub password or token, default anonymous")

    return argparser.parse_args()


if __name__ == "__main__":
    main()
