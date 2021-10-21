'''    This program allows user to query olympics database. User can query asking for
all the athletes who competed for a specific NOC, or list all NOCs by gold medals
won, or list all athletes who won a medal at a given games.

        Chris Melville
        Oct 20, 2021        '''
import sys
import psycopg2
import config


def main():

    connection = get_connection()

    if len(sys.argv) < 2:
        print('Use tag -h or --help for information on how to use this program.')

    elif sys.argv[1] == '-m' or sys.argv[1] == '--medals':
        if len(sys.argv) > 2:
            print(medals_help())
            exit()
        query = get_NOC_golds_query()
        print_NOC_golds(get_cursor(query, connection))

    elif sys.argv[1] == '-a' or sys.argv[1] == '--athletes':
        if len(sys.argv) > 3:
            print(athletes_help())
            exit()
        if not is_valid_NOC(sys.argv[2]):
            print('Please make sure to enter a valid NOC.')
            exit()
        query = get_NOC_athlete_query(sys.argv[2])
        print_NOC_athletes(get_cursor(query, connection))

    elif sys.argv[1] == '-g' or sys.argv[1] == '--games':
        if not is_valid_games(sys.argv):
            print(games_help())
            exit()
        query = get_games_medalists_query(sys.argv[2] + ' ' + sys.argv[3])
        print_games_medalists(get_cursor(query, connection))

    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('This program has 3 flags which can be used to search the olympics database.')
        print(athletes_help())
        print(games_help())
        print(medals_help())

    else:
        print('Use tag -h or --help for information on how to use this program.')

    connection.close()

def athletes_help():
    return 'The -a or --athletes flag returns all athletes who competed for a given NOC and only takes one argument: the NOC whose athletes are being searched.'

def games_help():
    return 'The -g or --games flag returns all athletes who medalled at a given olympic games and requires two arguments: a year and a season in which an Olympics took place.'

def medals_help():
    return 'The -m or --medals flag returns a list of all NOCs, in order of gold medals won, and does not accept any arguments.'

def print_NOC_golds(cursor):
    for row in cursor:
        print('NOC: '+row[0]+'    Gold Medals: '+str(row[1]))

def print_NOC_athletes(cursor):
    print('Athletes for specified NOC:')
    for row in cursor:
        print(row[1]+' '+row[2])

def print_games_medalists(cursor):
    print('Medalists at specified games:')
    for row in cursor:
        print(row[2]+' '+row[3])


def get_connection():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()
    return connection


def get_cursor(query, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    return cursor


def get_NOC_athlete_query(NOC_to_check):
    return 'SELECT DISTINCT athlete_games.athlete_id, athletes.given_name, athletes.surname, athlete_games.NOC FROM athlete_games, athletes WHERE athlete_games.NOC = \'' + NOC_to_check + '\' AND athlete_games.athlete_id = athletes.id ORDER BY athletes.surname, athletes.given_name'

def get_NOC_golds_query():
    medal_name = '\'Gold\''
    return 'SELECT NOCs.NOC, count(CASE WHEN medals.medal = ' + medal_name + ' THEN 1 ELSE NULL END) medals_count FROM NOCs, medals, athletes, athlete_games WHERE medals.athlete_games_id = athlete_games.id AND athlete_games.athlete_id = athletes.id AND NOCs.NOC = athlete_games.NOC GROUP BY NOCs.NOC ORDER BY medals_count DESC'

def get_games_medalists_query(games_to_check):
    medalless_string = 'NA'
    return 'SELECT DISTINCT athlete_games.athlete_id, athletes.given_name, athletes.surname, athlete_games.NOC FROM athletes, athlete_games, medals, games WHERE medals.medal != \'' + medalless_string + '\'AND medals.athlete_games_id = athlete_games.id AND athlete_games.athlete_id = athletes.id AND games.games = \'' + games_to_check + '\'AND games.id = athlete_games.games_id ORDER BY athlete_games.NOC, athletes.surname'

def is_valid_games(games_candidate):
    if len(games_candidate) != 4:
        return False
    year = games_candidate[2]
    season = games_candidate[3]
    try:
        year = int(year)
    except:
        return False
    if year%2 == 1 or year < 1896 or year > 2016:
        return False
    if season != 'Winter' and season != 'Summer':
        return False
    return True

def is_valid_NOC(NOC_candidate):
    cursor = get_cursor('SELECT NOCs.NOC FROM NOCs ORDER BY NOCs.NOC', get_connection())
    for row in cursor:
        if row[0] == NOC_candidate:
            return True
    return False

main()
