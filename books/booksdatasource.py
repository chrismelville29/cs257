#!/usr/bin/env python3
# Authors: Chris Melville and Jake Martens
# Revised by Chris Melville

'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv
import re

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __str__(self):
        return(self.surname + ', ' + self.given_name + ' ' + str(self.birth_year) + '-' + str(self.death_year))

    def is_equal(self, other_author):
        if self.__str__() == other_author.__str__():
            return True
        return False

    def contains_string(self, string_to_check):
        author_name = self.given_name + ' ' + self.surname
        match = re.search(string_to_check, author_name, re.IGNORECASE)
        if match != None:
            return True
        else:
            return False

    def get_author_name(self):
        return self.given_name + ' ' + self.surname

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __str__(self):
        author_string = self.authors[0].__str__()
        for i in range (1, len(self.authors)):
            author_string += ' and '+self.authors[i].__str__()
        return '{} ({}) by {}'.format(self.title, self.publication_year, author_string)

    def get_title(self):
        return self.title

    def contains_string(self, string_to_check):
        book_name = self.title
        match = re.search(string_to_check, book_name, re.IGNORECASE)
        if match != None:
            return True
        else:
            return False

    def get_publication_year(self):
        return self.publication_year

    def is_between_years(self, start_year, end_year):
        return self.is_before(end_year) and self.is_after(start_year)

    def is_after(self, year):
        if year == None:
            return True
        if self.publication_year >= year:
            return True
        return False

    def is_before(self, year):
        if year == None:
            return True
        if self.publication_year <= year:
            return True
        return False




class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.books_set = set()
        self.authors_set = set()
        self.load_data_from_csv(books_csv_file_name)

    def load_data_from_csv(self, books_csv_file_name):
        with open(books_csv_file_name,'r') as csv_file:

            for row in csv.reader(csv_file):
                curr_title = row[0]
                curr_publication_year = int(row[1])
                authors_of_book = []
                curr_authors = row[2].split(' and ')

                for author in curr_authors:
                    author_object = self.author_object_from_string(author)
                    if self.existing_author(author_object) != None:
                        author_object = self.existing_author(author_object)
                    else:
                        self.authors_set.add(author_object)
                    authors_of_book.append(author_object)

                curr_book = Book(curr_title, curr_publication_year, authors_of_book)
                self.books_set.add(curr_book)


    def author_object_from_string(self, author):
        list_for_given_name = author.split(' ',1)
        given_name = list_for_given_name[0]
        list_for_surname = list_for_given_name[1].split(' (')
        surname = list_for_surname[0]
        list_for_lifespan = list_for_surname[1].split('-')
        birth_year = int(list_for_lifespan[0])
        death_year = None
        if list_for_lifespan[1] != ')':
            death_year = int(list_for_lifespan[1].split(')')[0])
        author_as_object=Author(surname, given_name, birth_year, death_year)
        return author_as_object



    def existing_author(self, author_to_check):
        for author in self.authors_set:
            if author.is_equal(author_to_check):
                return author
        return None


    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        if search_text == None:
            search_text = ''
        authors_that_match = []
        for author in self.authors_set:
            if author.contains_string(search_text):
                authors_that_match.append(author)

        authors_that_match.sort(key = lambda x: x.__str__())

        return authors_that_match

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        if search_text == None:
            search_text = ''
        books_that_match = []
        for book in self.books_set:
            if book.contains_string(search_text):
                books_that_match.append(book)
        if sort_by == 'year':
            books_that_match.sort(key = lambda x: x.get_publication_year())
        else:
            books_that_match.sort(key = lambda x: x.__str__())

        return books_that_match

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        books_that_match = []
        if start_year != None:
            start_year = int(start_year);
        if end_year != None:
            end_year = int(end_year);
        for book in self.books_set:
            if book.is_between_years(start_year, end_year):
                books_that_match.append(book)

        books_that_match.sort(key = lambda x: (x.get_publication_year(), x.__str__()))
        return books_that_match
