let playerID = document.getElementsByName('player_id')[0].content;
let year = document.getElementsByName('year')[0].content;

function initialize() {
    loadPlayerYear();
}

window.onload = initialize;

function loadPlayerYear() {
    let url = getBaseURL() + '/api/player/' + playerID + '?year='+year;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(player_stats) {
        document.getElementById('player_name').innerHTML = player_stats['name']+' - '+player_stats['year'];
        document.getElementById('career_record').innerHTML = player_stats['record'];
        document.getElementById('highest_ranking').innerHTML = player_stats['highest_ranking'];
        document.getElementById('tournament_wins').innerHTML = player_stats['tournament_wins'];
        document.getElementById('breadcrumb').innerHTML = getBreadcrumbHTML(player_stats);
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
        tournament = tournaments[i];
        listContents+='<li><a href="'+getBaseURL()+'/tournament_year/'+tournament['id']+'">'+tournament['name']+'</a></li>';
    }
    return listContents;
}

function getBreadcrumbHTML(player_stats) {
    let baseURL = getBaseURL();
    let breadcrumb = '<a href="'+baseURL+'">Home</a> - ';
    breadcrumb+='<a href="'+baseURL+'/player/'+player_stats['id']+'">'+player_stats['name']+'</a>';
    return breadcrumb;
}


function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
