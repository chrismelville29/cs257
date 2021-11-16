function initialize() {
    let url = getAPIBaseURL() + '/player/' + playerID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(player_stats) {
        document.getElementById('player_name').innerHTML = 'JEFF'
    })
}

window.onload = initialize;


function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}
