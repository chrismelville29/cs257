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
    return get_sql_data(get_players_json, get_players_query(), ('%'+search_string+'%',))

@api.route('/tournaments/<search_string>')
def get_tournaments_from_search(search_string):
    return get_sql_data(get_tournaments_json, get_tournaments_query(), ('%'+search_string+'%',))


def get_connection():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()
    return connection

def get_cursor(query, connection, search_tuple):
    print(query)
    print(search_string)
    try:
        cursor = connection.cursor()
        cursor.execute(query,search_tuple)
    except Exception as e:
        print(e)
        exit()
    return cursor

def get_sql_data(getter, query, search_tuple):
    connection = get_connection()
    cursor = get_cursor(query, connection, search_tuple)
    data_to_return = getter(cursor)
    connection.close()
    return data_to_return

def get_players_json(cursor):
    player_list = []
    for row in cursor:
        player = {
        'id':row[0],
        'surname':row[1],
        'initials':row[2]}
        player_list.append(player)
    return json.dumps(player_list)

def get_player_stats_json(cursor):
    lowest_ranking = 1000
    for row in cursor:
        try:
            if int(row[0] < lowest_ranking):
                lowest_ranking = row[0]
        except:
            pass
    if lowest_ranking == 1000:
        return "NR"
    return str(lowest_ranking)

def get_tournament_wins(cursor):



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

def get_versus_query():
    return '''SELECT tournament_years.year, tournaments.name, players.surname, players.initials,
    matches.w_set_1, matches.l_set_1, matches.w_set_2, matches.l_set_2, matches.w_set_3, matches.l_set_3,
    matches.w_set_4, matches.l_set_4, matches.w_set_5, matches.l_set_5
    FROM tournament_years, tournaments, players, matches, player_tournaments
    WHERE players.id = 643
    AND matches.winner_id = player_tournaments.id
    AND player_tournaments.player_id = players.id
    AND player_tournaments.tournament_id = tournament_years.id
    AND tournament_years.tournament_id = tournaments.id;
    '''

def get_rankings_query():
    return '''SELECT player_tournaments.ranking
    FROM player_tournaments, players, tournament_years
    WHERE player_tournaments.player_id = players.id
    AND tournament_years.id = player_tournaments.tournament_id
    AND tournament_years.year < %s
    AND tournament_years.year > %s
    AND players.id = %s;'''

def get_tournament_wins_query():
    return '''SELECT count(CASE WHEN players.id = %s THEN 1 ELSE NULL END) wins
    FROM matches, player_tournaments, players
    WHERE player_tournaments.player_id = players.id
    AND matches.winner_id = player_tournaments.player_id
    AND matches.

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
