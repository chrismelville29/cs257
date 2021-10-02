# Authors: Chris Melville and Jake Martens

import booksdatasource
import argparse

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='The database to search.')
    parser.add_argument('-t','--title',const='', type = str, nargs = '?',help = 'Title of a book')
    parser.add_argument('-y','--year', action='store_true', help = 'Use with --title to sort by publication year')
    parser.add_argument('-a','--author', const='', type = str, nargs = '?', help = 'Author of a book')
    parser.add_argument('-d','--date',nargs=2, help = "Years between which book was published, e.g. 1850 1967. Use any string to indicate  to include any year")


    args = parser.parse_args()
    database = booksdatasource.BooksDataSource(args.filename)

    if args.title != None and args.author == None and args.date == None:
        print_matching_titles(args.title, database, args.year)

    elif args.title == None and args.author != None and args.date == None:
        print_matching_authors(args.author, database)

    elif args.title == None and args.author == None and args.date != None:
        print_books_between_years(args.date[0], args.date[1], database)

    else:
        parser.print_help()




main()
