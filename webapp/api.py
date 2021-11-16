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

@api.route('/player/<player_id>')
def get_player_stats(player_id):
    year = int(flask.request.args.get('year', default='0'))
    start_year = year-1
    end_year = year+1
    if year == 0:
        start_year = 1000
        end_year = 3000
    query_tuple = (start_year, end_year, int(player_id))
    tournament_wins = get_sql_data(get_tournament_wins, get_tournament_wins_query(), query_tuple)
    lowest_ranking = get_sql_data(get_lowest_ranking, get_lowest_ranking_query(), query_tuple)
    record = get_sql_data(get_record, get_record_query(), query_tuple)
    player_stats = {
    'name':get_sql_data(get_name_from_id, get_name_from_id_query(),(player_id,)),
    'tournament_wins':get_sql_data(get_tournament_wins, get_tournament_wins_query(), query_tuple),
    'highest_ranking':get_sql_data(get_lowest_ranking, get_lowest_ranking_query(), query_tuple),
    'record':get_sql_data(get_record, get_record_query(), query_tuple)}
    if year == 0:
        player_stats['years_active'] = get_sql_data(get_years_active, get_years_active_query(), (player_id,))
    else:
        player_stats['year'] = year
        player_stats['year_tournaments'] = get_sql_data(get_year_tournaments, get_year_tournaments_query(), (year,player_id))
    return json.dumps(player_stats)




def get_connection():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()
    return connection

def get_cursor(query, connection, search_tuple):
    #print(query)
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

def get_lowest_ranking(cursor):
    lowest_ranking = 1000
    for row in cursor:
        try:
            if int(row[0]) < lowest_ranking:
                lowest_ranking = int(row[0])
        except:
            pass
    if lowest_ranking == 1000:
        return "NR"
    return str(lowest_ranking)

def get_tournament_wins(cursor):
    for row in cursor:
        return str(row[0])

def get_record(cursor):
    for row in cursor:
        return str(row[0]) + ' - ' + str(row[1])

def get_years_active(cursor):
    years_active = []
    for row in cursor:
        years_active.append(row[0])
    return years_active

def get_name_from_id(cursor):
    for row in cursor:
        return row[1] + ' ' + row[0]

def get_year_tournaments(cursor):
    tournaments = []
    for row in cursor:
        tournaments.append(row[0])
    return tournaments






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

def get_lowest_ranking_query():
    return '''SELECT player_tournaments.ranking
    FROM player_tournaments, players, tournament_years
    WHERE player_tournaments.player_id = players.id
    AND tournament_years.id = player_tournaments.tournament_id
    AND tournament_years.year > %s
    AND tournament_years.year < %s
    AND players.id = %s
    ORDER BY player_tournaments.ranking DESC;'''

def get_tournament_wins_query():
    return '''SELECT count(CASE WHEN rounds.name = 'The Final' THEN 1 ELSE NULL END) wins
    FROM matches, player_tournaments, players, rounds, tournament_years
    WHERE player_tournaments.player_id = players.id
    AND tournament_years.year > %s
    AND tournament_years.year < %s
    AND players.id = %s
    AND matches.winner_id = player_tournaments.id
    AND matches.round_id = rounds.id
    AND player_tournaments.tournament_id = tournament_years.id;'''

def get_record_query():
    return '''SELECT count(CASE WHEN matches.winner_id = player_tournaments.id THEN 1 ELSE NULL END) wins,
    count(CASE WHEN matches.loser_id = player_tournaments.id THEN 1 ELSE NULL END) losses
    FROM matches, player_tournaments, players, tournament_years
    WHERE tournament_years.year > %s
    AND tournament_years.year < %s
    AND players.id = %s
    AND player_tournaments.tournament_id = tournament_years.id
    AND players.id = player_tournaments.player_id;'''

def get_years_active_query():
    return '''SELECT DISTINCT tournament_years.year
    FROM tournament_years, players, player_tournaments
    WHERE players.id = %s
    AND player_tournaments.player_id = players.id
    AND tournament_years.id = player_tournaments.tournament_id
    ORDER BY tournament_years.year ASC;'''

def get_year_tournaments_query():
    return '''SELECT tournaments.name
    FROM tournaments, player_tournaments, tournament_years, players
    WHERE tournament_years.year = %s
    AND players.id = %s
    AND players.id = player_tournaments.player_id
    AND player_tournaments.tournament_id = tournament_years.id
    AND tournament_years.tournament_id = tournaments.id
    ORDER BY tournaments.name;'''

def get_name_from_id_query():
    return '''SELECT players.surname, players.initials
    FROM players
    WHERE players.id = %s;'''
