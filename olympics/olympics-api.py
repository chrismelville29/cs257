'''
    olympics-api.py
    Chris Melville, 28 Oct 2021

    Manages an API which allows the user to query
    olympics.sql database
'''
import argparse
import flask
import json
import psycopg2
import config

app = flask.Flask(__name__)

@app.route('/')
@app.route('/help')
def introduction():
    return '''Hello and welcome to this olympics database searching API.
    You didn't tell us to make a usage statement, so I didn't. '''


@app.route('/games')
def games_route():
    return get_general_json(get_games_json, get_games_query())

@app.route('/nocs')
def nocs_route():
    return get_general_json(get_nocs_json, get_nocs_query())

@app.route('/medalists/games/<games_id>')
def medalists_route(games_id):
    noc = flask.request.args.get('noc', default='%')
    return get_general_json(get_medalists_json, get_medalists_query(str(games_id),noc))


'''Creates a cursor given a query, and calls one of the get_%_json functions
to convert the cursor into json form.'''

def get_general_json(getter, query):
    connection = get_connection()
    cursor = get_cursor(query, connection)
    json_to_return = getter(cursor)
    connection.close()
    return json_to_return


'''Given a cursor, the following three functions take the data from the cursor and
convert it to json form.'''

def get_games_json(cursor):
    games_list = []
    for row in cursor:
        games_name_split = row[1].split(' ')
        curr_games = {'id': row[0],
        'year': int(games_name_split[0]),
        'season': games_name_split[1],
        'city': row[2]}
        games_list.append(curr_games)
    return json.dumps(games_list)

def get_nocs_json(cursor):
    nocs_list = []
    for row in cursor:
        curr_noc = {'abbreviation': row[0],
        'name': row[1]}
        nocs_list.append(curr_noc)
    return json.dumps(nocs_list)

def get_medalists_json(cursor):
    medalists_list = []
    for row in cursor:
        athlete_full_name = row[1]+' '+row[2]
        curr_medalist = {'athlete_id': row[0],
        'athlete_name': athlete_full_name,
        'athlete_sex': row[3],
        'sport': row[4],
        'event': row[5],
        'medal': row[6]}
        medalists_list.append(curr_medalist)
    return json.dumps(medalists_list)


'''The following three methods return the SQL queries that the cursor needs to search
the contents of the olympics database.'''

def get_games_query():
    return '''SELECT games.id, games.games, games.city
    FROM games
    ORDER BY games.games;   '''

def get_nocs_query():
    return '''SELECT nocs.noc, nocs.region
    FROM nocs
    ORDER BY nocs.noc;  '''

def get_medalists_query(games_id, noc):
    return '''SELECT athletes.id, athletes.given_name, athletes.surname, athletes.sex, sports.sport, events.event, medals.medal
    FROM athletes, athlete_games, medals, sports, events, games
    WHERE games.id = '''+games_id+''' AND athletes.id = athlete_games.athlete_id
    AND athlete_games.id = medals.athlete_games_id
    AND medals.medal != 'NA'
    AND athlete_games.games_id = games.id
    AND athlete_games.noc LIKE '''+'\''+noc.upper()+'\''+''' AND medals.event_id = events.id
    AND events.sport_id = sports.id
    ORDER BY athletes.surname, athletes.given_name; '''


'''Both of the following methods work to extract data from the olympics database '''

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser('An API which lets the user query the olympics database')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
