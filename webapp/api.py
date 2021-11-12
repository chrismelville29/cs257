'''
    api.py
    Chris Melville and Nate Przybyla, November 9 2021

    Flask API to support ATP tour application
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

@api.route('/players/<search_string>')
def get_players_from_search(search_string):
    return get_general_json(get_players_json, get_players_query(), '%'+search_string+'%')

@api.route('/tournaments/<search_string>')
def get_tournaments_from_search(search_string):
    return get_general_json(get_tournaments_json, get_tournaments_query(), '%'+search_string+'%')


def get_connection():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()
    return connection

def get_cursor(query, connection, search_string):
    print(query)
    print(search_string)
    try:
        cursor = connection.cursor()
        cursor.execute(query,(search_string,))
    except Exception as e:
        print(e)
        exit()
    return cursor

def get_general_json(getter, query, search_string):
    connection = get_connection()
    cursor = get_cursor(query, connection, search_string)
    json_to_return = getter(cursor)
    connection.close()
    return json_to_return

def get_players_json(cursor):
    player_list = []
    for row in cursor:
        player = {
        'id':row[0],
        'surname':row[1],
        'initials':row[2]}
        player_list.append(player)
    return json.dumps(player_list)

def get_tournaments_json(cursor):
    tournament_list = []
    for row in cursor:
        tournament = {
        'id':row[0],
        'name':row[1],
        'location':row[2],
        'surface':row[3]}
        tournament_list.append(tournament)
    return json.dumps(tournament_list)



def get_players_query():
    return '''SELECT players.id, players.surname, players.initials
    FROM players
    WHERE LOWER(players.surname) LIKE LOWER(%s)
    ORDER BY players.surname, players.initials;   '''

def get_tournaments_query():
    return '''SELECT tournaments.id, tournaments.name, tournaments.location, surfaces.surface
    FROM tournaments, surfaces
    WHERE LOWER(tournaments.name) LIKE LOWER(%s)
    AND tournaments.surface_id = surfaces.id
    ORDER BY tournaments.name;  '''
