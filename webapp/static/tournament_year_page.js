let tournamentYearID = document.getElementsByName('tournament_year_id')[0].content;

function initialize() {
    loadTournamentYear();

    let playerButton = document.getElementById('player_search_button');
    playerButton.onclick = onPlayerSearchButton;

}

window.onload = initialize;

function loadTournamentYear() {
    let url = getBaseURL() + '/api/tournament_year/' + tournamentYearID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(tournament_year_info) {
        document.getElementById('tournament_name').innerHTML = tournament_year_info['name'];
        document.getElementById('surface').innerHTML = tournament_year_info['surface'];
        document.getElementById('location').innerHTML = tournament_year_info['location'];
        document.getElementById('champion').innerHTML = getChampionHTML(tournament_year_info['champion']);
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getChampionHTML(champion_info) {
    return '<a href="'+getBaseURL()+'/player_tournament/'+champion_info['id']+'">'+champion_info['name']+'</a>'
}

function getTournamentsHTML(tournaments) {
    let listContents = "";
    for(let i = 0; i < tournaments.length; i++) {
        listContents+="<li>"+tournaments[i]+"</li>";
    }
    return listContents;
}


function onPlayerSearchButton() {
    let playerString = document.getElementById('player_string');
    let url = getBaseURL() + '/api/players/' + playerString.value+'?tournament_year_id='+tournamentYearID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(players) {
        let listBody = '';
        for (let i = 0; i < players.length; i++) {
            let player = players[i];
            let linkText = player['name'];
            listBody += '<li><a href="/player_tournament/'+player['id']+'">'+linkText+'</a></li>';
        }

        document.getElementById('player_results').innerHTML=listBody;
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
