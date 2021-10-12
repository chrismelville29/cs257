# Authors: Chris Melville and Jake Martens
# Revised by Chris Melville


'''
    books.py
    Chris Melville & Jake Martens, September/October 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import booksdatasource
import argparse


'''
        All three of these functions use booksdatasource.py to create a list of books
        or authors given parameters from the command line and then print the results
'''
def print_matching_titles(title_to_check, database, sort_flag):
    if sort_flag:
        list_of_books = database.books(title_to_check, 'year')
    else:
        list_of_books = database.books(title_to_check)
    for book in list_of_books:
        print(book)

def print_matching_authors(author_to_check, database):
    list_of_authors = database.authors(author_to_check)
    for author in list_of_authors:
        print(author)

def print_books_between_years(start_year, end_year, database):
    list_of_books_between_years = database.books_between_years(start_year, end_year)
    for book in list_of_books_between_years:
        print(book)


'''
        Parses the command line to see which flags were raised, and then calls the
        print methods at the top of books.py to print the appropriate data given
        the parameters the user passed in
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='The csv file to search.')
    parser.add_argument('-t','--title',const='', type = str, nargs = '?',help = 'Title of a book')
    parser.add_argument('-y','--year', action='store_true', help = 'Use with --title to sort by publication year')
    parser.add_argument('-a','--author', const='', type = str, nargs = '?', help = 'Author of a book')
    parser.add_argument('-d','--date',type = str, nargs='*', help = "Years between which books were published, e.g. 1850 1967. Leave the second argument empty to include all years after the first date, or leave both blank for all books.")


    args = parser.parse_args()
    database = booksdatasource.BooksDataSource(args.filename)

    if args.author == None and args.date == None:
        print_matching_titles(args.title, database, args.year)

    elif args.title == None and args.author != None and args.date == None:
        print_matching_authors(args.author, database)

    elif args.title == None and args.author == None and args.date != None:
        if len(args.date) == 0:
            print_books_between_years(None,None,database)
        elif len(args.date) == 1:
            print_books_between_years(args.date[0], None, database)
        else:
            print_books_between_years(args.date[0], args.date[1], database)

    else:
        parser.print_help()




main()
