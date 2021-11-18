function initialize() {
    let playerButton = document.getElementById('player_search_button');
    playerButton.onclick = onPlayerSearchButton;

    let tournamentButton = document.getElementById('tournament_search_button');
    tournamentButton.onclick = onTournamentSearchButton;
}

window.onload = initialize;

function onPlayerSearchButton() {
    let playerStringElement = document.getElementById('player_string');
    let url = getAPIBaseURL() + '/players/' + playerStringElement.value

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(players) {
        let tableBody = '<tr> <th> Player Name </th> </tr>';
        for (let i = 0; i < players.length; i++) {
            let player = players[i];
            let linkText = player['name'];
            tableBody += '<tr><td><a href="/player/'+player['id']+'">'+linkText+'</a></td></tr>\n';
        }

        let playersTable = document.getElementById('player_results');
        if (playersTable) {
            playersTable.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });

}

function onTournamentSearchButton() {
    let tournamentStringElement = document.getElementById('tournament_string');
    let url = getAPIBaseURL() + '/tournaments/' + tournamentStringElement.value

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(tournaments) {
        let tableBody = '<tr><th> Tournament Name </th><th> Location </th><th> Surface </th></tr>';
        for (let i = 0; i < tournaments.length; i++) {
            let tournament = tournaments[i];
            tableBody += '<tr><td>' + tournament['name'] + '</td><td>' + tournament['location'] + '</td><td>' + tournament['surface'] + '</td></tr>\n';
        }

        let tournamentsTable = document.getElementById('tournament_results');
        if (tournamentsTable) {
            tournamentsTable.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });

}

function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}
