#!/usr/bin/env python3

""" Reads a repo tree from GitHub, then produces a json file ready to be
    imported into analyze-catalog for the BIEL website. """

import argparse
import json
import operator
import pathlib
import sys
import urllib

import github

def main():
    """ Main function. """
    extensions = ["pdf", "docx", "zip"]
    args = parse_arguments()
    books = load_books()
    github_api = get_github_api(args.user, args.password)
    repo = github_api.get_repo("wa-biel/biel-files")
    tree = repo.get_git_tree("master", recursive=True)
    biel_data = create_biel_data_from_tree(tree, extensions, books)
    json.dump(biel_data, args.outfile, sort_keys=True, indent=4)

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

def load_books():
    """ Load books.json from disk """
    with open("books.json") as infile:
        return json.load(infile)

def get_github_api(username, password):
    """ Logs into GitHub and returns an api object. If username and
        password are both blank, then an anonymous login will be used. """
    if (username == "" and password == ""):
        github_api = github.Github()
    else:
        github_api = github.Github(username, password)
    return github_api

def create_biel_data_from_tree(tree, extensions, books):
    """ Reads the repo tree and returns a BIEL-formatted data object. """
    files = filter_files_from_tree(tree, extensions, books)
    data = create_biel_data_from_files(files)
    return data

def filter_files_from_tree(tree, extensions, books):
    """ Reads a GitHub tree object and returns a list of files to be
        included in BIEL, sorted by name. """
    files = {}
    for entry in tree.tree:
        path_parts = pathlib.Path(entry.path).parts

        # Ignore anything outside the review guide
        if path_parts[0] != "review-guide":
            continue

        # Ignore files that don't end with the given extensions
        filename_root = None
        filename_extension = None
        filename = path_parts[-1]
        for extension in extensions:
            if filename.endswith(extension):
                filename_root = filename[:(len(extension)*-1)-1]
                filename_extension = extension
                break # for extension in extensions
        if filename_root is None:
            continue

        # Process files
        if filename_root not in files:
            # If the filename is a book of the Bible, sort in canonical order
            book_number = ""
            if filename_root in books:
                book_number = str(books[filename_root]["num"]).zfill(2)
            # Sort shallower items before deeper ones, then by directory
            sort = str(len(path_parts)) + \
                   "/".join(path_parts[2:-1] + \
                   (book_number + filename_root,))
            files[filename_root] = {
                "sort": sort,
                "name": filename_root,
                "root": filename_root,
                "links": {}
                }
        file_data = files[filename_root]
        file_data["links"][filename_extension] = {
            "filename": filename,
            "extension": filename_extension,
            "path": entry.path,
            }
    return sorted(files.values(), key=operator.itemgetter("sort"))

def create_biel_data_from_files(files):
    """ Creates BIEL-formatted data from list of files. """
    data = []

    # Create node for English
    en_node = {}
    en_node["code"] = "en"
    en_node["contents"] = []
    en_node_contents = en_node["contents"]
    data.append(en_node)

    # Create node for Reviewer's Guide
    rg_node = {}
    rg_node["code"] = "rg"
    rg_node["name"] = "Reviewer's Guide"
    rg_node["subject"] = "Reference"
    rg_node["checkingLevel"] = "3"
    rg_node["links"] = []
    rg_node["subcontents"] = []
    en_node_contents.append(rg_node)

    # Create nodes for each file
    subcontents = rg_node["subcontents"]
    sort = 0
    for file_data in files:
        sort += 1
        entry = {
            "name": file_data["name"],
            "code": "",
            "sort": sort,
            "category": "topics",
            "links": []
            }
        print(file_data["sort"])
        for link in sorted(file_data["links"].values(), key=operator.itemgetter("extension")):
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
    """ Returns a URL for the given path that will download the file from the repo. """
    return "https://github.com/wa-biel/biel-files/raw/master/" + urllib.parse.quote(path)

if __name__ == "__main__":
    main()
