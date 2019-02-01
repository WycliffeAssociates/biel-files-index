""" Tests for main.py """

import unittest
from unittest.mock import Mock

import main

class TestMain(unittest.TestCase):
    """ Tests for main.py """

    def test_create_biel_data_from_tree(self):
        """ Create BIEL data from GitHub tree """
        # pylint: disable=line-too-long
        tree = Mock(tree=[
            Mock(path="not-in-review-guide/dir1/dir2/Example Guide.pdf"),
            Mock(path="review-guide/dir1/dir2/Guide for Genesis.docx"),
            Mock(path="review-guide/dir1/dir2/Guide for Genesis.pdf"),
            Mock(path="review-guide/dir1/dir2/Example Guide.ignored-extension"),
            Mock(path="review-guide/dir1/dir2/Example Guide.pdf"),
            Mock(path="review-guide/dir1/dir2/Example Guide.docx"),
            ])
        extensions = ["pdf", "docx", "zip"]
        books = {"Genesis": {"num": 1, "anth": "ot"}}
        expected = [{
            "code": "en",
            "contents": [{
                "checkingLevel": "3",
                "code": "rg",
                "links": [],
                "name": "Reviewer's Guide",
                "subject": "Reference",
                "subcontents": [
                    {"name": "Example Guide",
                     "code": "",
                     "sort": 1,
                     "category": "topics",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/review-guide/dir1/dir2/Example%20Guide.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []},
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/review-guide/dir1/dir2/Example%20Guide.pdf",
                          "format": "pdf",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    {"name": "Guide for Genesis",
                     "code": "",
                     "sort": 2,
                     "category": "topics",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/review-guide/dir1/dir2/Guide%20for%20Genesis.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []},
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/review-guide/dir1/dir2/Guide%20for%20Genesis.pdf",
                          "format": "pdf",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    ]}]}]
        actual = main.create_biel_data_from_tree(tree, extensions, books)
        self.assertEqual(expected, actual)
