let tournamentID = document.getElementsByName('tournament_id')[0].content;

function initialize() {
    loadTournament();
}

window.onload = initialize;

function loadTournament() {
    let url = getBaseURL() + '/api/tournament/' + tournamentID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(tournament_info) {
        document.getElementById('tournament_name').innerHTML = tournament_info['name'];
        document.getElementById('surface').innerHTML = tournament_info['surface'];
        document.getElementById('location').innerHTML = tournament_info['location'];
        let tournamentYearsHTML = getTournamentYearsHTML(tournament_info['years_held']);
        document.getElementById('years_held').innerHTML = tournamentYearsHTML;
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getTournamentYearsHTML(years) {
    let listContents = "";
    let baseURL = getBaseURL();
    for(let i = 0; i < years.length; i++) {
        let year = years[i];
        let link = '<li><a href="'+getBaseURL()+'/tournament_year/'+year['id']+'">'+year['year']+'</a></li>';
        listContents+=link;
    }
    return listContents;
}

function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
