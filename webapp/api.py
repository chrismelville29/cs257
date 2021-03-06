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

@api.route('/help')
def get_help():
    return flask.render_template('help_page.html')

@api.route('/players/<search_string>')
def get_players_from_search(search_string):
    tournament_year_id = int(flask.request.args.get('tournament_year_id', default = '-1'))
    if tournament_year_id == -1:
        return get_sql_data(get_players_json, get_players_query(), ('%'+search_string+'%',))
    return get_sql_data(get_players_json, get_player_tournaments_query(), (tournament_year_id,'%'+search_string+'%'))

@api.route('/tournaments/<search_string>')
def get_tournaments_from_search(search_string):
    return get_sql_data(get_tournaments_json, get_tournaments_query(), ('%'+search_string+'%',))

@api.route('/player/<player_id>')
def get_player_stats(player_id):
    year = int(flask.request.args.get('year', default='0'))
    return get_player_stats_json(year, player_id)

@api.route('/tournament/<tournament_id>')
def get_tournament_info(tournament_id):
    return get_tournament_info_json(tournament_id)

@api.route('/tournament_year/<tournament_year_id>')
def get_tournament_year_info(tournament_year_id):
    round_id = int(flask.request.args.get('round_id', default='-1'))
    if round_id == -1:
        return get_tournament_year_info_json(tournament_year_id)
    return get_tournament_round_json(tournament_year_id, round_id)


@api.route('/player_tournament/<player_tournament_id>')
def get_player_tournament_matches(player_tournament_id):
    return get_player_tournament_info_json(player_tournament_id)



def get_connection():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()
    return connection

def get_cursor(query, connection, search_tuple):
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
        'name':row[2]+' '+row[1]}
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


def get_player_stats_json(year, player_id):
    start_year = year-1
    end_year = year+1
    if year == 0:
        start_year = 1000
        end_year = 3000
    query_tuple = (start_year, end_year, int(player_id))
    player_stats = {
    'id':player_id,
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

def get_tournament_info_json(tournament_id):
    tournament_info = {
    'name':get_sql_data(get_name_from_id, get_tournament_name_from_id_query(), (tournament_id,)),
    'surface':get_sql_data(get_name_from_id, get_surface_from_id_query(), (tournament_id,)),
    'location':get_sql_data(get_name_from_id, get_location_from_id_query(), (tournament_id,)),
    'years_held':get_sql_data(get_years_held, get_tournament_years_query(), (tournament_id,))
    }
    return json.dumps(tournament_info)

def get_tournament_year_info_json(tournament_year_id):
    champion = get_sql_data(get_tournament_champ, get_tournament_champ_query(), (tournament_year_id,))
    tournament_year_info = {
    'id':int(tournament_year_id),
    'tournament_id':get_sql_data(get_name_from_id, get_tournament_from_year_query(),(tournament_year_id,)),
    'name':get_sql_data(get_name_from_id, get_tournament_year_from_id_query(),(tournament_year_id,)),
    'surface':get_sql_data(get_name_from_id, get_surface_from_year_query(),(tournament_year_id,)),
    'location':get_sql_data(get_name_from_id, get_location_from_year_query(),(tournament_year_id,)),
    'champion':champion,
    'rounds':get_sql_data(get_rounds,get_rounds_query(),(champion['id'],))
    }
    return json.dumps(tournament_year_info)


def get_player_tournament_info_json(player_tournament_id):
    player_tournament_info = {
    'self_info':get_sql_data(get_player, get_player_tournament_from_id_query(),(player_tournament_id,)),
    'losers':get_sql_data(get_opponents, get_losers_query(), (player_tournament_id,)),
    'winners':get_sql_data(get_opponents, get_winners_query(), (player_tournament_id,)),
    'tournament':get_sql_data(get_tournament_from_player, get_tournament_year_query(), (player_tournament_id,))
    }
    return json.dumps(player_tournament_info)

def get_tournament_round_json(tournament_year_id, round_id):
    match_ids = get_sql_data(get_match_ids_by_round, get_round_query(), (round_id,tournament_year_id))
    matches = get_matches_by_round(match_ids)
    round_information = {
    }
    return json.dumps(matches)






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
        years_active.append(str(row[0]))
    return years_active

def get_name_from_id(cursor):
    for row in cursor:
        try:
            return str(row[1]) + ' ' + row[0]
        except:
            return row[0]

def get_year_tournaments(cursor):
    tournaments = []
    for row in cursor:
        tournament = {
        'id':row[0],
        'name':row[1]
        }
        tournaments.append(tournament)
    return tournaments

def get_years_held(cursor):
    years = []
    for row in cursor:
        year = {
        'id':row[0],
        'year':row[1]
        }
        years.append(year)
    return years

def get_player(cursor):
    for row in cursor:
        player = {
        'id':row[0],
        'name':row[2]+' '+row[1]
        }
        return player

def get_opponents(cursor):
    matches_list = []
    for row in cursor:
        match = {
        'opponent_name': row[2]+ ' '+ row[1],
        'opponent_id': row[0],
        'score': get_score_string(row,4),
        'round': row[3]
        }
        matches_list.append(match)
    return matches_list

def get_score_string(row, start_index):
    score_string = row[start_index]+'-'+row[start_index+1]
    for i in range(start_index,start_index+8,2):
        if row[i] == '':
            break
        score_string += ', '+row[i]+'-'+row[i+1]
    return score_string

def get_tournament_from_player(cursor):
    for row in cursor:
        tournament = {
        'id':row[2],
        'year_id':row[3],
        'name':row[0],
        'year_name':str(row[1])+' '+row[0]
        }
        return tournament

def get_rounds(cursor):
    rounds = []
    for row in cursor:
        round = {
        'id':row[0],
        'name':row[1]
        }
        rounds.append(round)
    return rounds

def get_tournament_champ(cursor):
    for row in cursor:
        champ = {
        'id':row[0],
        'name':row[2]+' '+row[1]
        }
    return champ

def get_match_ids_by_round(cursor):
    matches = []
    for row in cursor:
        match = {
        'round_name':row[0],
        'winner_id':row[1],
        'loser_id':row[2],
        'score':get_score_string(row,3)
        }
        matches.append(match)
    return matches

def get_matches_by_round(matches_ids):
    matches = []
    for match_id in matches_ids:
        match = {
        'round_name':match_id['round_name'],
        'winner':get_sql_data(get_player,get_player_from_player_tournament_id_query(), (match_id['winner_id'],)),
        'loser':get_sql_data(get_player,get_player_from_player_tournament_id_query(), (match_id['loser_id'],)),
        'score':match_id['score']
        }
        matches.append(match)
    return matches








def get_players_query():
    return '''SELECT players.id, players.surname, players.initials
    FROM players
    WHERE LOWER(players.surname) LIKE LOWER(%s)
    ORDER BY players.surname, players.initials;   '''

def get_players_at_tournament_query():
    return '''SELECT player_tournaments.id, players.surname, players.initials
    FROM players, player_tournaments
    WHERE LOWER(players.surname) LIKE LOWER(%s)
    AND players.id = player_tournaments.player_id
    AND player_tournaments.tournament_id = %s; '''

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
    return '''SELECT tournament_years.id, tournaments.name
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

def get_player_tournament_from_id_query():
    return '''SELECT players.id, players.surname, players.initials
    FROM players, player_tournaments
    WHERE player_tournaments.id = %s
    AND player_tournaments.player_id = players.id;'''

def get_player_from_player_tournament_id_query():
    return '''SELECT player_tournaments.id, players.surname, players.initials
    FROM players, player_tournaments
    WHERE player_tournaments.id = %s
    AND player_tournaments.player_id = players.id;'''

def get_tournament_name_from_id_query():
    return '''SELECT tournaments.name
    FROM tournaments
    WHERE tournaments.id = %s;'''

def get_tournament_year_from_id_query():
    return '''SELECT tournaments.name, tournament_years.year
    FROM tournaments, tournament_years
    WHERE tournament_years.id = %s
    AND tournament_years.tournament_id = tournaments.id;'''

def get_surface_from_id_query():
    return '''SELECT surfaces.surface
    FROM surfaces, tournaments
    WHERE tournaments.id = %s
    AND tournaments.surface_id = surfaces.id;'''

def get_surface_from_year_query():
    return '''SELECT surfaces.surface
    FROM surfaces, tournaments, tournament_years
    WHERE surfaces.id = tournaments.surface_id
    AND tournaments.id = tournament_years.tournament_id
    AND tournament_years.id = %s;'''

def get_location_from_id_query():
    return '''SELECT tournaments.location
    FROM tournaments
    WHERE tournaments.id = %s;'''

def get_location_from_year_query():
    return '''SELECT tournaments.location
    FROM tournaments, tournament_years
    WHERE tournaments.id = tournament_years.tournament_id
    AND tournament_years.id = %s;'''

def get_tournament_years_query():
    return '''SELECT tournament_years.id, tournament_years.year
    FROM tournaments, tournament_years
    WHERE tournaments.id = %s
    AND tournaments.id = tournament_years.tournament_id;'''

def get_tournament_from_year_query():
    return '''SELECT tournaments.id
    FROM tournaments, tournament_years
    WHERE tournament_years.id = %s
    AND tournament_years.tournament_id = tournaments.id;'''

def get_player_tournaments_query():
    return '''SELECT player_tournaments.id, players.surname, players.initials
    FROM player_tournaments, players, tournament_years
    WHERE tournament_years.id = player_tournaments.tournament_id
    AND tournament_years.id = %s
    AND LOWER(players.surname) LIKE LOWER(%s)
    AND players.id = player_tournaments.player_id
    ORDER BY players.surname;'''

def get_losers_query():
    return '''SELECT players.id, players.surname, players.initials, rounds.name,
    matches.w_set_1, matches.l_set_1, matches.w_set_2, matches.l_set_2, matches.w_set_3,
    matches.l_set_3, matches.w_set_4, matches.l_set_4, matches.w_set_5, matches.l_set_5
    FROM players, player_tournaments, matches, rounds
    WHERE rounds.id = matches.round_id
    AND players.id = player_tournaments.player_id
    AND matches.loser_id = player_tournaments.id
    AND matches.winner_id = %s
    ORDER BY rounds.name;'''

def get_winners_query():
    return '''SELECT players.id, players.surname, players.initials, rounds.name,
    matches.w_set_1, matches.l_set_1, matches.w_set_2, matches.l_set_2, matches.w_set_3,
    matches.l_set_3, matches.w_set_4, matches.l_set_4, matches.w_set_5, matches.l_set_5
    FROM players, player_tournaments, matches, rounds
    WHERE rounds.id = matches.round_id
    AND players.id = player_tournaments.player_id
    AND matches.winner_id = player_tournaments.id
    AND matches.loser_id = %s;'''

def get_tournament_year_query():
    return '''SELECT tournaments.name, tournament_years.year, tournaments.id, tournament_years.id
    FROM tournaments, tournament_years, player_tournaments
    WHERE player_tournaments.id = %s
    AND player_tournaments.tournament_id = tournament_years.id
    AND tournament_years.tournament_id = tournaments.id;'''

def get_rounds_query():
    return '''SELECT rounds.id, rounds.name
    FROM rounds, matches
    WHERE rounds.id = matches.round_id
    AND matches.winner_id = %s
    ORDER BY rounds.name;'''

def get_tournament_champ_query():
    return '''SELECT player_tournaments.id, players.surname, players.initials
    FROM players, player_tournaments, matches, tournament_years, rounds
    WHERE rounds.name = 'The Final'
    AND tournament_years.id = %s
    AND matches.round_id = rounds.id
    AND tournament_years.id = player_tournaments.tournament_id
    AND players.id = player_tournaments.player_id
    AND matches.winner_id = player_tournaments.id;'''

def get_round_query():
    return '''SELECT rounds.name, matches.winner_id, matches.loser_id, matches.w_set_1, matches.l_set_1,
    matches.w_set_2, matches.l_set_2, matches.w_set_3, matches.l_set_3, matches.w_set_4,
    matches.l_set_4, matches.w_set_5, matches.l_set_5
    FROM matches, rounds, player_tournaments, tournament_years
    WHERE rounds.id = %s
    AND rounds.id = matches.round_id
    AND matches.winner_id = player_tournaments.id
    AND player_tournaments.tournament_id = tournament_years.id
    AND tournament_years.id = %s;'''
