#!/usr/bin/env python3

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
            Mock(path="en/not-in-review-guide/dir1/dir2/Example Guide.pdf"),
            Mock(path="en/review-guide/dir1/dir2/Guide for 1 John.pdf"),
            Mock(path="en/review-guide/dir1/dir2/Guide for 1 John.docx"),
            Mock(path="en/review-guide/dir1/dir2/Guide for Numbers.docx"),
            Mock(path="en/review-guide/dir1/dir2/Guide for Numbers.pdf"),
            Mock(path="en/review-guide/dir1/dir2/Guide for Matthew.docx"),
            Mock(path="en/review-guide/dir1/dir2/Guide for Matthew.pdf"),
            Mock(path="en/review-guide/dir1/dir2/Guide for Genesis.docx"),
            Mock(path="en/review-guide/dir1/dir2/Guide for Genesis.pdf"),
            Mock(path="en/review-guide/dir1/dir2/Guide for BrokenBook.docx"),
            Mock(path="en/review-guide/dir1/dir2/Example Guide.ignored-extension"),
            Mock(path="en/review-guide/dir1/dir2/Example Guide.pdf"),
            Mock(path="en/review-guide/dir1/dir2/Example Guide.docx"),
            ])
        extensions = ["pdf", "docx", "zip"]
        books = {
            "Genesis": {"num": 1, "anth": "ot"},
            "Numbers": {"num": 4, "anth": "ot"},
            "Matthew": {"num": 41, "anth": "nt"},
            "1 John": {"num": 63, "anth": "nt"},
            "BrokenBook": {"num": 68, "anth": "broken"}}
        expected = [{
            "code": "en",
            "contents": [{
                "checkingLevel": "3",
                "code": "rg",
                "links": [],
                "name": "Reviewers' Guide",
                "subject": "Reference",
                "subcontents": [
                    {"name": "Example Guide",
                     "code": "",
                     "sort": 1,
                     "category": "topics",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Example%20Guide.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []},
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Example%20Guide.pdf",
                          "format": "pdf",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    {"name": "Guide for Genesis",
                     "code": "",
                     "sort": 2,
                     "category": "bible-ot",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%20Genesis.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []},
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%20Genesis.pdf",
                          "format": "pdf",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    {"name": "Guide for Numbers",
                     "code": "",
                     "sort": 3,
                     "category": "bible-ot",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%20Numbers.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []},
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%20Numbers.pdf",
                          "format": "pdf",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    {"name": "Guide for Matthew",
                     "code": "",
                     "sort": 4,
                     "category": "bible-nt",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%20Matthew.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []},
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%20Matthew.pdf",
                          "format": "pdf",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    {"name": "Guide for 1 John",
                     "code": "",
                     "sort": 5,
                     "category": "bible-nt",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%201%20John.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []},
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%201%20John.pdf",
                          "format": "pdf",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    {"name": "Guide for BrokenBook",
                     "code": "",
                     "sort": 6,
                     "category": "topics",
                     "links": [
                         {"url":
                          "https://github.com/wa-biel/biel-files/raw/master/en/review-guide/dir1/dir2/Guide%20for%20BrokenBook.docx",
                          "format": "docx",
                          "zipContent": "",
                          "quality": None,
                          "chapters": []}]},
                    ]}]}]
        files = main.filter_files_from_tree(tree, "en", "review-guide", extensions, books)
        actual = main.create_biel_data_from_tree(
            files, "wa-biel", "biel-files", "master", "en", "Reviewers' Guide")
        self.assertEqual(expected, actual)

    def test_calculate_sort_field_john(self):
        """ Test that books sort in the correct order """
        en_index = 0
        languages = main.load_json("languages.json")
        books = languages[en_index]["books"]
        self.assertEqual("5-dir1/dir2/44-John Guide", main.calculate_sort_field(("en",
            "review-guide", "dir1", "dir2", "John Guide.pdf"), "John Guide", books))
        self.assertEqual("5-dir1/dir2/63-1 John Guide", main.calculate_sort_field(("en",
            "review-guide", "dir1", "dir2", "1 John Guide.pdf"), "1 John Guide", books))
        self.assertEqual("5-dir1/dir2/64-2 John Guide", main.calculate_sort_field(("en",
            "review-guide", "dir1", "dir2", "2 John Guide.docx"), "2 John Guide", books))
        self.assertEqual("5-dir1/dir2/65-3 John Guide", main.calculate_sort_field(("en",
            "review-guide", "dir1", "dir2", "3 John Guide.docx"), "3 John Guide", books))



if __name__ == "__main__": # pragma: no cover
    unittest.main()
