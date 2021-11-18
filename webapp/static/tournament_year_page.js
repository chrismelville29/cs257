let playerID = document.getElementsByName('tournament_id')[0].content;
let year = document.getElementsByName('year')[0].content;

function initialize() {
    loadTournamentYear();

    let playerButton = document.getElementById('player_search_button');
    playerButton.onclick = onPlayerSearchButton;

}

function loadTournamentYear() {
    let url = getBaseURL() + '/api/tournament/' + tournamentID + '?year='+year;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(tournament_info) {
        document.getElementById('tournament_name').innerHTML = tournament_info['year']+' '+tournament_info['name'];
        let tournamentsHTML = getTournamentsHTML(player_stats['year_tournaments']);
        document.getElementById('tournaments').innerHTML = tournamentsHTML;
    })

    .catch(function(error) {
        console.log(error);
    });
}
window.onload = initialize;

function getTournamentsHTML(tournaments) {
    let listContents = "";
    for(let i = 0; i < tournaments.length; i++) {
        listContents+="<li>"+tournaments[i]+"</li>";
    }
    return listContents;
}


function onPlayerSearchButton() {
    let playerStringElement = document.getElementById('player_string');
    let url = getBaseURL() + '/api/players/' + playerStringElement.value

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(players) {
        let tableBody = '<tr> <th> Player Name </th> </tr>';
        for (let i = 0; i < players.length; i++) {
            let player = players[i];
            let linkText = player['initials']+' '+player['surname'];
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


function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
