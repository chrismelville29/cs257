

'''This program will read in the athletes_events.csv file from kaggle
and then output csv files that will be read into a postgresql database.
The noc_regions.csv file can be left as is so this program will not touch it.
Chris Melville, Oct 14'''

'''Note on the project as a whole - I couldn't figure out the SQL query for the
NOCs gold medals question.'''


import csv

class Team:
    def __init__(self, id, team):
        self.id = id
        self.team = team

    def __eq__(self, other_team):
        return self.team == other_team.get_team()

    def __str__(self):
        return str(self.id)+','+self.team

    def to_csv(self):
        return [self.id, self.team]

    def get_id(self):
        return self.id
    def get_team(self):
        return self.team

class Games:
    def __init__(self, id, games, city):
        self.id = id
        self.games = games
        self.city = city

    def __eq__(self, other_games):
        return self.games == other_games.get_games()

    def __str__(self):
        return str(self.id)+','+self.games+','+self.city

    def to_csv(self):
        return [self.id, self.games, self.city]

    def get_id(self):
        return self.id
    def get_games(self):
        return self.games
    def get_city(self):
        return self.city

class Sport:
    def __init__(self, id, sport):
        self.id = id
        self.sport = sport

    def __eq__(self, other_sport):
        return self.sport == other_sport.get_sport()

    def __str__(self):
        return str(self.id)+','+self.sport

    def to_csv(self):
        return [self.id, self.sport]

    def get_id(self):
        return self.id
    def get_sport(self):
        return self.sport

class Event:
    def __init__(self, id, sport_id, event):
        self.id = id
        self.event = event
        self.sport_id = sport_id

    def __eq__(self, other_event):
        return self.event == other_event.get_event()

    def __str__(self):
        return str(self.id)+','+str(self.sport_id)+','+self.event

    def to_csv(self):
        return [self.id, self.sport_id, self.event]

    def get_id(self):
        return self.id
    def get_event(self):
        return self.event
    def get_sport_id(self):
        return self.sport_id

class Athlete_Games:
    def __init__(self, id, athlete_id, games_id, team_id, age, height, weight, NOC):
        self.id = id
        self.athlete_id = athlete_id
        self.games_id = games_id
        self.age = age
        self.height = height
        self.weight = weight
        self.NOC = NOC
        self.team_id = team_id

    def __eq__(self, other_athlete_games):
        if other_athlete_games == None:
            return False
        return self.athlete_id == other_athlete_games.get_athlete_id() and self.games_id == other_athlete_games.get_games_id()

    def __str__(self):
        return str(self.id)+','+str(self.athlete_id)+','+str(self.games_id)+','+str(self.team_id)+','+self.age+','+self.height+','+self.weight+','+self.NOC

    def to_csv(self):
        return [self.id, self.athlete_id, self.games_id, self.team_id, self.age, self.height, self.weight, self.NOC]

    def get_id(self):
        return self.id
    def get_athlete_id(self):
        return self.athlete_id
    def get_games_id(self):
        return self.games_id
    def get_age(self):
        return self.age
    def get_height(self):
        return self.height
    def get_weight(self):
        return self.weight
    def get_NOC(self):
        return self.NOC
    def get_team_id(self):
        return self.team_id

class Athlete:
    def __init__(self, id, surname, given_name, sex):
        self.id = id
        self.surname = surname
        self.given_name = given_name
        self.sex = sex

    def __eq__(self, other_athlete):
        if other_athlete == None:
            return False
        return self.id == other_athlete.get_id()

    def __str__(self):
        return str(self.id)+','+self.surname+','+self.given_name+','+self.sex

    def to_csv(self):
        return [self.id, self.surname, self.given_name, self.sex]


    def get_id(self):
        return self.id
    def get_surname(self):
        return self.surname
    def get_given_name(self):
        return self.given_name
    def get_sex(self):
        return self.sex

class Medal:
    def __init__(self, athlete_games_id, event_id, medal):
        self.athlete_games_id = athlete_games_id
        self.event_id = event_id
        self.medal = medal

    def __str__(self):
        return str(self.athlete_games_id)+','+str(self.event_id)+','+self.medal

    def to_csv(self):
        return [self.athlete_games_id, self.event_id, self.medal]

    def get_athlete_games_id(self):
        return self.athlete_games_id
    def get_event_id(self):
        return self.event_id
    def get_medal(self):
        return self.medal


class OlympicsDataSource:
    def __init__(self, olympics_csv):
        self.athletes_list = []
        self.teams_list = []
        self.games_list = []
        self.events_list = []
        self.sports_list = []
        self.athlete_games_list = []
        self.medals_list = []

        self.load_data_from_csv(olympics_csv)
        self.write_data_to_csv('teams.csv',self.teams_list)
        self.write_data_to_csv('athletes.csv',self.athletes_list)
        self.write_data_to_csv('games.csv',self.games_list)
        self.write_data_to_csv('events.csv',self.events_list)
        self.write_data_to_csv('sports.csv',self.sports_list)
        self.write_data_to_csv('athlete_games.csv',self.athlete_games_list)
        self.write_data_to_csv('medals.csv',self.medals_list)




    '''Takes the data from the csv file and uses it to populate the sets at the top
    of the __init__ method.
    '''
    def load_data_from_csv(self, olympics_csv):
        with open(olympics_csv) as csv_file:
            next(csv_file)
            counter = 0
            for row in csv.reader(csv_file):
                counter+=1
                if counter % 30003 == 0:
                    print('progressing thru reading csv file - you\'ll see 8 or 9 of these')
                self.convert_row_to_objects(row)
        print('done reading csv file')

    def write_data_to_csv(self, file_to_write, data_list):
        with open(file_to_write, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in data_list:
                csv_writer.writerow(item.to_csv())
        print('Finished writing file for:  '+file_to_write)

    ''' Converts the row into objects, and then adds the objects to their respective sets
    if they are distinct from the objects currently in the set
    '''
    def convert_row_to_objects(self, row):
        athlete_name = self.split_name(row[1])
        curr_athlete = self.existing_object_for_athlete(self.athletes_list,Athlete(int(row[0]),athlete_name[1],athlete_name[0],row[2]))
        curr_team = self.existing_object_not_athlete(self.teams_list,Team(len(self.teams_list),row[6]))
        curr_sport = self.existing_object_not_athlete(self.sports_list,Sport(len(self.sports_list),row[12]))
        curr_event = self.existing_object_not_athlete(self.events_list,Event(len(self.events_list),curr_sport.get_id(),row[13]))
        curr_games = self.existing_object_not_athlete(self.games_list,Games(len(self.games_list),row[8],row[11]))
        curr_athlete_games = self.existing_object_for_athlete(self.athlete_games_list,Athlete_Games(len(self.athlete_games_list),curr_athlete.get_id(),curr_games.get_id(),curr_team.get_id(),row[3],row[4],row[5],row[7]))
        self.medals_list.append(Medal(curr_athlete_games.get_id(),curr_event.get_id(),row[14]))



    def split_name(self, name):
        athlete_names = name.split(' ')
        athlete_name = ['','']
        #if len(athlete_names) == 0:
        #    athlete_names = ['','']
        athlete_name[1] = athlete_names.pop()
        athlete_name[0] = ' '.join(athlete_names)
        return athlete_name


    '''The following methods check to see if an object has been seen before. If it has,
    they return the existing object, otherwise add the object being checked to the
    appropriate list and return it
    '''

    def existing_object_not_athlete(self, set_to_search, object_to_find):
        for curr_object in set_to_search:
            if curr_object == object_to_find:
                return curr_object
        set_to_search.append(object_to_find)
        return object_to_find

    def existing_object_for_athlete(self,set_to_search, object_to_find):
        compare_object = None
        if not len(set_to_search) == 0:
            compare_object = set_to_search[len(set_to_search)-1]
        if object_to_find == compare_object:
            return compare_object
        set_to_search.append(object_to_find)
        return object_to_find

def main():
    my_source = OlympicsDataSource('athlete_events.csv')


main()
