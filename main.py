#!/usr/bin/env python3

""" Reads a repo tree from GitHub, then produces a json file ready to be
    imported into analyze-catalog for the BIEL website. """

import json
import operator
import os
import pathlib
import sys
import urllib

import github

class ApplicationException(Exception):
    """ Base class for application exceptions """

def main(): # pragma: no cover
    """ Main function. """
    extensions = ["pdf", "docx", "zip"]
    config = read_config()
    languages = load_json("languages.json")
    github_api = get_github_api(config["github_username"], config["github_password"])
    repo = github_api.get_repo(f"{config['repo_username']}/{config['repo_id']}")
    tree = repo.get_git_tree(config["branch_id"], recursive=True)
    data = []
    for language in languages:
        files = filter_files_from_tree(
            tree,
            language["lang_code"],
            language["dir_name"],
            extensions,
            language["books"])
        data += create_biel_data_from_tree(
            files,
            config["repo_username"],
            config["repo_id"],
            config["branch_id"],
            language["lang_code"],
            language["dir_label"])
    json.dump(data, sys.stdout, sort_keys=True, indent=4)

def read_config(): # pragma: no cover
    """ Read configuration from environment """
    return {
        "github_username": get_env("BF_GITHUB_USERNAME"),
        "github_password": get_env("BF_GITHUB_PASSWORD"),
        "repo_username":   get_env("BF_REPO_USERNAME", raise_exception=True),
        "repo_id":         get_env("BF_REPO_ID", raise_exception=True),
        "branch_id":       get_env("BF_BRANCH_ID", raise_exception=True)
        }

def get_env(env_var_name, raise_exception=False): # pragma: no cover
    """ Get environment variable, optionally throwing an exception if not defined. """
    if env_var_name in os.environ:
        return os.environ[env_var_name]
    if raise_exception:
        raise ApplicationException(f"{env_var_name} not defined")
    return ""

def load_json(filename): # pragma: no cover
    """ Load json file from disk """
    with open(filename) as infile:
        return json.load(infile)

def get_github_api(username, password): #pragma: no cover
    """ Logs into GitHub and returns an api object. If username and
        password are both blank, then an anonymous login will be used. """
    if (username == "" and password == ""):
        github_api = github.Github()
    else:
        github_api = github.Github(username, password)
    return github_api

def filter_files_from_tree(tree, language_code, dir_name, extensions, books):
    """ Reads a GitHub tree object and returns a list of files to be
        included in BIEL, sorted by name. """
    files = {}
    for entry in tree.tree:
        path_parts = pathlib.Path(entry.path).parts

        # Ignore anything outside the review guide
        if len(path_parts) < 2 or \
           path_parts[0] != language_code or \
           path_parts[1] != dir_name:
            continue

        # Ignore files that don't end with the given extensions
        filename_root = None
        filename_extension = None
        filename = path_parts[-1]
        for extension in extensions:
            if filename.endswith(extension):
                # Calculate offset of extension (plus period) from end of string
                filename_root = filename[:(len(extension) + 1) * -1]
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
                "category": calculate_category(filename_root, books),
                "links": {}
                }

        # Add link to file in index
        files[filename_root]["links"][filename_extension] = {
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

def create_biel_data_from_tree(files, repo_username, repo_id, branch_id, language_code, dir_label):
    # pylint: disable=too-many-arguments
    """ Reads the repo tree and returns a BIEL-formatted data object. """
    return [{
        "code": language_code,
        "contents": [{
            "checkingLevel": "3",
            "code": "rg",
            "links": [],
            "name": dir_label,
            "subject": "Reference",
            "subcontents": create_subcontents(repo_username, repo_id, branch_id, files)}]}]


def calculate_category(filename_root, books):
    """ Calculate which category the file should be placed in.  At the time
        of this comment the translations_page.js recognizes the following
        categories:

        - 'bible-ot'
        - 'bible-nt'
        - 'obs'
        - 'topics'
        - 'other'

        books is a dictionary (defined in languages.json) where the key is
        the book name, and has a field "anth" which tells which anthology
        the book is found in: "ot" or "nt".
        """
    category = "topics"
    for book_name in books:
        if book_name in filename_root:
            if books[book_name]["anth"] == "ot":
                category = "bible-ot"
            elif books[book_name]["anth"] == "nt":
                category = "bible-nt"
            break
    return category


def calculate_sort_field(path_parts, filename_root, books):
    """ Calculate where this item should be sorted.  Returns a string that
        can be used to naturally sort the files.

        books is a dictionary (defined in languages.json) where the key is
        the book name, and has a field "num" which can be used to sort in
        canonical order.
        """

    # Create index of book names in order from longest to shortest.  This
    # is to ensure that books with shorter similar names don't accidentally
    # get matched before longer ones, e.g. "1 John" being matches as
    # "John".
    book_names_by_length = sorted(list(books), key=len, reverse=True)

    # If the filename contains a book of the Bible, sort in canonical order
    book_number = "00-"
    for book in book_names_by_length:
        if book in filename_root:
            book_number = str(books[book]["num"]).zfill(2) + "-"
            break

    # Sort shallower items before deeper ones, then by directory
    sort = str(len(path_parts)) + "-" + \
            "/".join(path_parts[2:] + (book_number + filename_root,))

    return sort

def create_subcontents(repo_username, repo_id, branch_id, files):
    """ Creates subcontents nodes of output data """
    return [create_subcontents_entry(repo_username, repo_id, branch_id, file_data) \
                for file_data in files]

def create_subcontents_entry(repo_username, repo_id, branch_id, file_data):
    """ Create single subcontents node for a given file """
    return {
        "name": file_data["name"],
        "code": "",
        "sort": file_data["sort_index"],
        "category": file_data["category"],
        "links": [create_subcontents_entry_link(repo_username, repo_id, branch_id, link) \
                  for link in sorted(file_data["links"].values(), \
                                     key=operator.itemgetter("extension"))]}

def create_subcontents_entry_link(repo_username, repo_id, branch_id, link):
    """ Create link node """
    return {
        "url": path_to_url(repo_username, repo_id, branch_id, link["path"]),
        "format": link["extension"],
        "zipContent": "",
        "quality": None,
        "chapters": []
        }

def path_to_url(repo_username, repo_id, branch_id, path):
    """ Returns a URL for the given path that will download the file from the repo. """
    quoted_path = urllib.parse.quote(path)
    return f"https://github.com/{repo_username}/{repo_id}/raw/{branch_id}/{quoted_path}"

if __name__ == "__main__": # pragma: no cover
    main()
