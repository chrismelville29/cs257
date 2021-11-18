let playerID = document.getElementsByName('player_id')[0].content;
let year = document.getElementsByName('year')[0].content;

function initialize() {
    loadPlayerYear();
}

window.onload = initialize;

function loadPlayerYear() {
    let url = getAPIBaseURL() + '/player/' + playerID + '?year='+year;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(player_stats) {
        document.getElementById('player_name').innerHTML = player_stats['name']+' - '+player_stats['year'];
        document.getElementById('career_record').innerHTML = player_stats['record'];
        document.getElementById('highest_ranking').innerHTML = player_stats['highest_ranking'];
        document.getElementById('tournament_wins').innerHTML = player_stats['tournament_wins'];
        let tournamentsHTML = getTournamentsHTML(player_stats['year_tournaments']);
        document.getElementById('tournaments').innerHTML = tournamentsHTML;
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getTournamentsHTML(tournaments) {
    let listContents = "";
    for(let i = 0; i < tournaments.length; i++) {
        listContents+="<li>"+tournaments[i]+"</li>";
    }
    return listContents;
}


function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}
