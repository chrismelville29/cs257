CREATE TABLE teams (
id integer,
team text
);

CREATE TABLE games (
id integer,
games text,
city text
);

CREATE TABLE sports (
id integer,
sport text
);

CREATE TABLE events (
id integer,
sport_id integer,
event text
);

CREATE TABLE athlete_games (
id integer,
athlete_id integer,
games_id integer,
team_id integer,
age text,
height text,
weight text,
NOC text
);

CREATE TABLE athletes (
id integer,
surname text,
given_name text,
sex text
);

CREATE TABLE medals (
athlete_games_id integer,
event_id integer,
medal text
);

