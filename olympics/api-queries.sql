SELECT games.id, games.games, games.city
FROM games
ORDER BY games.games;

SELECT nocs.noc, nocs.region
FROM nocs
ORDER BY nocs.noc;

SELECT athletes.id, athletes.given_name, athletes.surname, athletes.sex, medals.medal, sports.sport, events.event
FROM athletes, athlete_games, medals, sports, events, nocs
WHERE games_id = 11
AND athletes.id = athlete_games.athlete_id
AND medals != 'NA'
AND athlete_games.noc = 'KEN'
AND medals.athlete_games_id = athlete_games.id
AND medals.event_id = events.id
AND events.sport_id = sport.id;
