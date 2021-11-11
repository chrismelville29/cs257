function initialize() {
    let button = document.getElementById('player_search_button');
    button.onclick = onPlayerSearchButton;
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
            tableBody += '<tr>' + '<td>' + player['initials'] + ' ' + player['surname'] + '</td>' + '</tr>\n';
        }

        // Put the table body we just built inside the table that's already on the page.
        let booksTable = document.getElementById('player_results');
        if (booksTable) {
            booksTable.innerHTML = tableBody;
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
