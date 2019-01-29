#!/usr/bin/env python3

import argparse
import json
import operator
import pathlib
import sys
import urllib

import github

def main():
    args = parse_arguments()
    github_api = login_to_github(args.user, args.password)
    repo = github_api.get_repo("wa-biel/biel-files")
    tree = repo.get_git_tree("master",recursive=True)
    biel_data = get_biel_data(tree)
    json.dump(biel_data,args.outfile, sort_keys=True, indent=4)

def parse_arguments(): # pragma: no cover
    """ Configures and parses command-line arguments """

    argparser = argparse.ArgumentParser(
        description="Prints index for biel-files GitHub repo")

    argparser.add_argument("--user",
                           nargs="?",
                           default="",
                           help="GitHub user, default anonymous")

    argparser.add_argument("--password",
                           nargs="?",
                           default="",
                           help="GitHub password or token, default anonymous")

    argparser.add_argument("--outfile",
                           nargs="?",
                           type=argparse.FileType("w"),
                           default=sys.stdout,
                           help="Filename of JSON output file, default stdout")

    return argparser.parse_args()

def login_to_github(username, password):
    if (username == "" and password == ""):
        github_api = github.Github()
    else:
        github_api = github.Github(username, password)
    return github_api

def get_biel_data(tree):
    files = {}
    for entry in tree.tree:
        path_parts = pathlib.Path(entry.path).parts
        # Ignore anything outside the review guide
        if (path_parts[0] != "review-guide"):
            continue
        # Only consider .docx and .pdf files
        filename = path_parts[-1]
        filename_root = None
        filename_extension = None
        if filename[-4:] == ".pdf":
            filename_root = filename[:-4]
            filename_extension = filename[-3:]
        if filename[-5:] == ".docx":
            filename_root = filename[:-5]
            filename_extension = filename[-4:]
        if filename_root is None:
            continue
        if filename_root not in files:
            files[filename_root] = {
                "sort": "/".join(path_parts[:-1]) + "/" + filename_root,
                "name": " / ".join(path_parts[2:-1]) + " / " + filename_root,
                "root": filename_root,
                "links": {}
                }
        file_data = files[filename_root]
        file_data["links"][filename_extension] = {
            "filename": filename,
            "extension": filename_extension,
            "path": entry.path,
            }
    data = []
    en = {}
    data.append(en)
    en["code"] = "en"
    en["contents"] = []
    en_contents = en["contents"]
    rg = {}
    en_contents.append(rg)
    rg["code"] = "rg"
    rg["name"] = "Reviewer's Guide"
    rg["subject"] = "Reference"
    rg["checkingLevel"] = "3"
    rg["links"] = []
    rg["subcontents"] = []
    subcontents = rg["subcontents"]
    sort = 0
    for file_data in sorted(files.values(), key=operator.itemgetter("sort")):
        sort += 1
        entry = {
            "name": file_data["name"],
            "code": "",
            "sort": sort,
            "category": "topics",
            "links": []
            }
        for link in file_data["links"].values():
            entry["links"].append({
                    "url": path_to_url(link["path"]),
                    "format": link["extension"],
                    "zipContent": "",
                    "quality": None,
                    "chapters": []
                    })
        subcontents.append(entry)
    return data

def path_to_url(path):
    return "https://github.com/wa-biel/biel-files/raw/master/" + urllib.parse.quote(path)

if __name__ == "__main__":
    main()
