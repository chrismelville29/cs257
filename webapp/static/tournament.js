function initialize() {
    let tournamentID = document.getElementsByName('tournament_id')[0].content;
    let url = getAPIBaseURL() + '/tournament/' + tournamentID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .catch(function(error) {
        console.log(error);
    });
}

window.onload = initialize;


function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}