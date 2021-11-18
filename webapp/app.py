'''
    app.py
    Chris Melville and Nate Przybyla

    A small Flask application that supports a little tennis webpage
'''
import flask
import argparse
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/')
def load_homepage():
    return flask.render_template('homepage.html')

@app.route('/player/<player_id>')
def load_player_page(player_id):
    year = int(flask.request.args.get('year', default='0'))
    if year == 0:
        return flask.render_template('player_page.html',player_id = player_id)
    return flask.render_template('player_year_page.html',player_id = player_id, year = str(year))

@app.route('/tournament/<tournament_id>')
def load_tournament_page(tournament_id):
    year = int(flask.request.args.get('year', default='0'))
    if year == 0:
        return flask.render_template('tournament_page.html', tournament_id = tournament_id)
    return flask.render_template('tournament_year_page.html', tournament_id=tournament_id, year = str(year))

@app.route('/tournament_year/<tournament_year_id>')
def load_tournament_year_page(tournament_year_id):
    return flask.render_template('tournament_year_page.html',tournament_year_id=tournament_year_id)

@app.route('/player_tournament/<player_tournament_id>')
def load_player_tournament_page(player_tournament_id):
    return flask.render_template('player_tournament_page.html',player_tournament_id=player_tournament_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tennis application, including API & DB')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
