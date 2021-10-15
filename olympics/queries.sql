SELECT athletes.surname, athletes.given_name, games.games, events.event, medals.medal
FROM athletes, games, athlete_games, medals, events
WHERE athletes.surname LIKE '%Louganis%'
AND athletes.given_name LIKE '%Greg%'
AND athletes.id = athlete_games.athlete_id
AND athlete_games.games_id = games.id
AND medals.athlete_games_id = athlete_games.id
AND events.id = medals.event_id
ORDER BY games.games, events.event;


SELECT NOCs.NOC
FROM NOCs
ORDER BY NOCs.NOC;

SELECT DISTINCT athlete_games.athlete_id, athletes.given_name, athletes.surname, athlete_games.NOC
FROM athlete_games, athletes
WHERE athlete_games.NOC = 'KEN'
AND athlete_games.athlete_id = athletes.id
ORDER BY athletes.surname, athletes.given_name;

SELECT athletes.surname, athletes.given_name, medals.medal
FROM medals, athletes, athlete_games
WHERE medals.medal = 'Gold'
AND medals.athlete_games_id = athlete_games.id
AND athlete_games.athlete_id = athletes.id;
