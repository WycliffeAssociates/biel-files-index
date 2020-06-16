#!/usr/bin/env python3

""" Reads a repo tree from GitHub, then produces a json file ready to be
    imported into analyze-catalog for the BIEL website. """

import argparse
import json
import operator
import os
import pathlib
import sys
import urllib

import github

def main(): # pragma: no cover
    """ Main function. """
    extensions = ["pdf", "docx", "zip"]
    config = read_config()
    books = load_books()
    github_api = get_github_api(config["github_username"], config["github_password"])
    repo = github_api.get_repo("wa-biel/biel-files")
    tree = repo.get_git_tree("master", recursive=True)
    biel_data = create_biel_data_from_tree(tree, extensions, books)
    json.dump(biel_data, sys.stdout, sort_keys=True, indent=4)

def read_config():
    config = {
        "github_username": "",
        "github_password": ""
        }

    if "BF_GITHUB_USERNAME" in os.environ:
        config["github_username"] = os.environ["BF_GITHUB_USERNAME"]

    if "BF_GITHUB_PASSWORD" in os.environ:
        config["github_password"] = os.environ["BF_GITHUB_PASSWORD"]

    return config

def load_books(): # pragma: no cover
    """ Load books.json from disk """
    with open("books.json") as infile:
        return json.load(infile)

def get_github_api(username, password): #pragma: no cover
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
    return [{
        "code": "en",
        "contents": [{
            "checkingLevel": "3",
            "code": "rg",
            "links": [],
            "name": "Reviewers' Guide",
            "subject": "Reference",
            "subcontents": create_subcontents(files)}]}]

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
                # Calculate offset of extension (plus period) from end of string
                extension_offset_from_end = (len(extension) + 1) * -1
                filename_root = filename[:extension_offset_from_end]
                filename_extension = extension
                break # for extension in extensions
        if filename_root is None:
            continue

        # Add file to index if it's not already there
        if filename_root not in files:
            files[filename_root] = {
                "sort": calculate_sort_field(path_parts, filename_root, books),
                "name": filename_root,
                "root": filename_root,
                "links": {}
                }

        # Add link to file in index
        file_data = files[filename_root]["links"][filename_extension] = {
            "filename": filename,
            "extension": filename_extension,
            "path": entry.path,
            }

    # Sort all the files by sort parameter
    file_list = sorted(files.values(), key=operator.itemgetter("sort"))

    # Now that we have the sorted list, calculate sort indexes
    sort_index = 0
    for file_data in file_list:
        sort_index += 1
        file_data["sort_index"] = sort_index

    return file_list

def calculate_sort_field(path_parts, filename_root, books):
    """ Calculate where this item should be sorted.  Returns a string that
        can be used to naturally sort the files. """

    # If the filename contains a book of the Bible, sort in canonical order
    book_number = "00-"
    for book in books:
        if book in filename_root:
            book_number = str(books[book]["num"]).zfill(2) + "-"
            break

    # Sort shallower items before deeper ones, then by directory
    sort = str(len(path_parts)) + "-" + \
           "/".join(path_parts[2:-1] + (book_number + filename_root,))

    return sort

def create_subcontents(files):
    """ Creates subcontents nodes of output data """
    return [create_subcontents_entry(file_data) for file_data in files]

def create_subcontents_entry(file_data):
    """ Create single subcontents node for a given file """
    return {
        "name": file_data["name"],
        "code": "",
        "sort": file_data["sort_index"],
        "category": "topics",
        "links": [create_subcontents_entry_link(link) \
                  for link in sorted(file_data["links"].values(), \
                                     key=operator.itemgetter("extension"))]}

def create_subcontents_entry_link(link):
    """ Create link node """
    return {
        "url": path_to_url(link["path"]),
        "format": link["extension"],
        "zipContent": "",
        "quality": None,
        "chapters": []
        }

def path_to_url(path):
    """ Returns a URL for the given path that will download the file from the repo. """
    return "https://github.com/wa-biel/biel-files/raw/master/" + urllib.parse.quote(path)

if __name__ == "__main__": # pragma: no cover
    main()
