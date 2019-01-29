#!/usr/bin/env python3
import argparse

import github

def main():
    args = parse_arguments()
    if (args.user == "" and args.password == ""):
        github_api = github.Github()
    else:
        github_api = github.Github(args.user, args.password)
    repo = github_api.get_repo("wa-biel/biel-files")
    tree = repo.get_git_tree("master",recursive=True)
    print(tree)
    print(tree.tree)

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
                           help="GitHub password, default anonymous")

    return argparser.parse_args()


if __name__ == "__main__":
    main()
