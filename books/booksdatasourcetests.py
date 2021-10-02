#Chris Melville and Jake Martens
'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source_long = booksdatasource.BooksDataSource('books1.csv')
        self.data_source_short = booksdatasource.BooksDataSource('books2.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source_long.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0].get_author_name() == 'Terry Pratchett')

    def test_authors_none(self):
        authors = self.data_source_short.authors(None)
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0].get_author_name() == 'Ann Brontë')
        self.assertTrue(authors[1].get_author_name() == 'Charlotte Brontë')
        self.assertTrue(authors[2].get_author_name() == 'Connie Willis')

    def test_author_sort(self):
        authors = self.data_source_short.authors('Brontë')
        self.assertTrue(len(authors) == 2)
        self.assertTrue(authors[0].get_author_name() == 'Ann Brontë')
        self.assertTrue(authors[1].get_author_name() == 'Charlotte Brontë')

    def test_case_insensitivity(self):
        authors = self.data_source_short.authors('willis')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0].get_author_name() == 'Connie Willis')

    def test_author_not_on_list(self):
        authors = self.data_source_short.authors('Agatha')
        self.assertTrue(len(authors) == 0)

    def test_unique_book(self):
        books = self.data_source_long.books('Sula')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].get_title() == 'Sula')

    def test_book_not_in_file(self):
        books = self.data_source_long.books('Cat')
        self.assertTrue(len(books) == 0)

    def test_books_none(self):
        books = self.data_source_short.books(None)
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].get_title() == 'All Clear')
        self.assertTrue(books[1].get_title() == 'Jane Eyre')
        self.assertTrue(books[2].get_title() == 'The Tenant of Wildfell Hall')

    def test_year_sorting(self):
        books = self.data_source_short.books('All', 'year')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0].get_title() == 'The Tenant of Wildfell Hall')
        self.assertTrue(books[1].get_title() == 'All Clear')

    def test_title_sorting_explicit(self):
        books = self.data_source_short.books('All', 'title')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0].get_title() == 'All Clear')
        self.assertTrue(books[1].get_title() == 'The Tenant of Wildfell Hall')

    def test_title_sorting_default(self):
        books = self.data_source_short.books('All')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0].get_title() == 'All Clear')
        self.assertTrue(books[1].get_title() == 'The Tenant of Wildfell Hall')

    def test_books_between_none(self):
        books = self.data_source_short.books_between_years()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].get_title() == 'Jane Eyre')
        self.assertTrue(books[1].get_title() == 'The Tenant of Wildfell Hall')
        self.assertTrue(books[2].get_title() == 'All Clear')

    def test_books_between_tiebreaker(self):
        books = self.data_source_long.books_between_years(1995,1996)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0].get_title() == 'Neverwhere')
        self.assertTrue(books[1].get_title() == 'Thief of Time')

    def test_books_between_no_end(self):
        books = self.data_source_long.books_between_years(2020, None)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0].get_title() == 'Boys and Sex')
        self.assertTrue(books[1].get_title() == 'The Invisible Life of Addie LaRue')

    def test_books_between_no_start(self):
        books = self.data_source_long.books_between_years(None,1770)
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].get_title() == 'The Life and Opinions of Tristram Shandy, Gentleman')

if __name__ == '__main__':
    unittest.main()
