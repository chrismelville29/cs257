'''This program will read in the data.csv file from kaggle
and then output csv files that will be read into a postgresql database.
Chris Melville and Nate Przybyla, Nov 2'''

import csv

class Surface:
    def __init__(self, id, surface):
        self.id = id
        self.surface = surface

    def __eq__(self, other_surface):
        return self.surface[0:3] == other_surface.surface[0:3]

    def to_csv(self):
        return [self.id,self.surface]

    def get_id(self):
        return self.id
    def get_surface(self):
        return self.surface

class Tournament:
    def __init__(self, id, name, location, surface_id):
        self.id = id
        self.name = name
        self.location = location
        self.surface_id = surface_id

    def __eq__(self, other_tournament):
        return self.name == other_tournament.get_name()

    def to_csv(self):
        return [self.id, self.name, self.location, self.surface_id]

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name

class Tournament_Year:
    def __init__(self, id, tournament_id, year):
        self.id = id
        self.tournament_id = tournament_id
        self.year = year

    '''This only works in conjunction with the corresponding existing_object method,
    otherwise same tournament different year would return true '''
    def __eq__(self, other_tournament_year):
        return self.tournament_id == other_tournament_year.get_tournament_id()

    def to_csv(self):
        return [self.id, self.tournament_id, self.year]

    def get_id(self):
        return self.id
    def get_tournament_id(self):
        return self.tournament_id
    def get_name(self):
        return self.name

class Player:
    def __init__(self, id, surname, initials):
        self.id = id
        self.surname = surname
        self.initials = initials

    def __eq__(self, other_player):
        return self.surname.lower() == other_player.get_surname().lower() and self.initials == other_player.get_initials()

    def to_csv(self):
        return [self.id, self.surname, self.initials]

    def get_id(self):
        return self.id
    def get_surname(self):
        return self.surname
    def get_initials(self):
        return self.initials

class Player_Tournament:
    def __init__(self, id, player_id, tournament_id, ranking):
        self.id = id
        self.player_id = player_id
        self.tournament_id = tournament_id
        self.ranking = ranking

    def __eq__(self, other_player_tournament):
        return self.player_id == other_player_tournament.player_id and self.tournament_id == other_player_tournament.tournament_id

    def to_csv(self):
        return [self.id, self.player_id, self.tournament_id, self.ranking]

    def get_id(self):
        return self.id
    def get_player_id(self):
        return self.player_id
    def get_tournament_id(self):
        return self.tournament_id

class Match:
    def __init__(self, winner_id, loser_id, w_set_1, l_set_1, w_set_2, l_set_2, w_set_3, l_set_3, w_set_4, l_set_4, w_set_5, l_set_5):
        self.winner_id = winner_id
        self.loser_id = loser_id
        self.w_set_1 = w_set_1
        self.l_set_1 = l_set_1
        self.w_set_2 = w_set_2
        self.l_set_2 = l_set_2
        self.w_set_3 = w_set_3
        self.l_set_3 = l_set_3
        self.w_set_4 = w_set_4
        self.l_set_4 = l_set_4
        self.w_set_5 = w_set_5
        self.l_set_5 = l_set_5

    def to_csv(self):
        return [self.winner_id, self.loser_id, self.w_set_1, self.l_set_1, self.w_set_2, self.l_set_2, self.w_set_3, self.l_set_3, self.w_set_4, self.l_set_4, self.w_set_5, self.l_set_5]

class TennisDataSource:
    def __init__(self, tennis_csv):
        self.surface_list = []
        self.tournament_list = []
        self.tournament_year_list = []
        self.player_list = []
        self.player_tournament_list = []
        self.match_list = []
        self.temp_player_tournament_list = []

        self.load_data_from_csv(tennis_csv)
        self.write_data_to_csv('surfaces.csv',self.surface_list)
        self.write_data_to_csv('tournaments.csv',self.tournament_list)
        self.write_data_to_csv('tournament_years.csv',self.tournament_year_list)
        self.write_data_to_csv('players.csv',self.player_list)
        self.write_data_to_csv('player_tournaments.csv',self.player_tournament_list)
        self.write_data_to_csv('matches.csv',self.match_list)

    '''Takes the data from the csv file and uses it to populate the sets at the top
    of the __init__ method.'''
    def load_data_from_csv(self, tennis_csv):
        with open(tennis_csv) as csv_file:
            next(csv_file)
            counter = 0
            last_tournament = "-1"
            for row in csv.reader(csv_file):
                counter+=1
                if counter%5000 == 0:
                    print('Rows processed (out of ~45k): '+str(counter))
                if last_tournament != row[0]:
                    self.new_tournament()
                last_tournament = row[0]
                self.convert_row_to_objects(row)
        print('done reading csv file')

    def write_data_to_csv(self, file_to_write, data_list):
        with open(file_to_write, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in data_list:
                csv_writer.writerow(item.to_csv())
        print('Finished writing file for:  '+file_to_write)

    ''' Converts the row into objects, and then adds the objects to their respective sets
    if they are distinct from the objects currently in the set'''
    def convert_row_to_objects(self, row):
        winner_name = self.split_name(row[9])
        loser_name = self.split_name(row[10])
        curr_surface = self.existing_object(self.surface_list, Surface(len(self.surface_list), row[6]))
        curr_tournament = self.existing_object(self.tournament_list, Tournament(len(self.tournament_list),self.strip_valencia_open(row[2]),row[1],curr_surface.get_id()))
        curr_tournament_year = self.existing_tournament_year(self.tournament_year_list, Tournament_Year(len(self.tournament_year_list),curr_tournament.get_id(),row[3].split('/')[2]))
        curr_winner = self.existing_object(self.player_list, Player(len(self.player_list),winner_name[0],winner_name[1]))
        curr_loser = self.existing_object(self.player_list, Player(len(self.player_list),loser_name[0],loser_name[1]))
        curr_winner_tournament = self.existing_object(self.temp_player_tournament_list, Player_Tournament(len(self.player_tournament_list)+len(self.temp_player_tournament_list),curr_winner.get_id(),curr_tournament_year.get_id(),row[11]))
        curr_loser_tournament = self.existing_object(self.temp_player_tournament_list, Player_Tournament(len(self.player_tournament_list)+len(self.temp_player_tournament_list),curr_loser.get_id(),curr_tournament_year.get_id(),row[12]))
        self.match_list.append(Match(curr_winner_tournament.get_id(),curr_loser_tournament.get_id(),row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22]))


    '''Checks to see if an object has been seen before. If it has,return the
    existing object, otherwise add the object being checked to the
    appropriate list and return it'''
    def existing_object(self, list_to_search, object_to_find):
        for curr_object in list_to_search:
            if curr_object == object_to_find:
                return curr_object
        list_to_search.append(object_to_find)
        return object_to_find

    def existing_tournament_year(self, list_to_search, object_to_find):
        if len(list_to_search) == 0:
            list_to_search.append(object_to_find)
        if list_to_search[-1] == object_to_find:
            return list_to_search[-1]
        list_to_search.append(object_to_find)
        return object_to_find

    def transfer_player_tournaments(self):
        for player in self.temp_player_tournament_list:
            self.player_tournament_list.append(player)

    def new_tournament(self):
        self.transfer_player_tournaments()
        self.temp_player_tournament_list = []

    def split_name(self, name):
        if name[-1] == ' ':
            name = name[0:-1]
        if name[-1] != '.':
            name += '.'
        athlete_names = name.split(' ')
        athlete_name = ['','']
        athlete_name[1] = athlete_names.pop()
        athlete_name[0] = ' '.join(athlete_names)
        return athlete_name

    ''' Valencia Open naming is weird, this fixes it '''
    def strip_valencia_open(self, tournament_name):
        if tournament_name[0:13] == 'Valencia Open':
            return 'Valencia Open'
        return tournament_name


def main():
    my_source = TennisDataSource('data.csv')

main()
