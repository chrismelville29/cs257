function initialize() {
    let tournamentID = document.getElementsByName('tournament_id')[0].content;
    let url = getAPIBaseURL() + '/tournament/' + tournamentID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(tournament_info) {
        document.getElementById('tournament_name').innerHTML = tournament_info['name'];
        document.getElementById('surface').innerHTML = tournament_info['surface'];
        document.getElementById('location').innerHTML = tournament_info['location'];
    })

    .catch(function(error) {
        console.log(error);
    });
}

window.onload = initialize;

function getTournamentYearsHTML(years) {
    
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}