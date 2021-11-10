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

@api.route('/')
def get_players_from_search():
    return get_general_json(get_players_json(), get_players_query(), 'Dj')
    

def get_connection():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()
    return connection

def get_cursor(query, connection, search_string):
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





def get_players_query():
    return '''SELECT players.surname, players.initials
    FROM players
    WHERE LOWER(players.surname) LIKE LOWER(%s)
    ORDER BY players.surname, players.initials;   '''
