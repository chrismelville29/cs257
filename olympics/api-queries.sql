SELECT games.id, games.games, games.city
FROM games
ORDER BY games.games;

SELECT nocs.noc, nocs.region
FROM nocs
ORDER BY nocs.noc;

SELECT athletes.id, athletes.given_name, athletes.surname, athletes.sex, sports.sport, events.event, medals.medal
FROM athletes, athlete_games, medals, sports, events, games
WHERE games.id = 11
AND athletes.id = athlete_games.athlete_id
AND athlete_games.id = medals.athlete_games_id
AND medals.medal != 'NA'
AND athlete_games.games_id = games.id
AND athlete_games.noc LIKE '%'
AND medals.event_id = events.id
AND events.sport_id = sports.id
ORDER BY athletes.surname, athletes.given_name;
