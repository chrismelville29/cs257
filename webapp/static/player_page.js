let playerID = document.getElementsByName('player_id')[0].content;

function initialize() {
    loadPlayer();
}

window.onload = initialize;

function loadPlayer() {
    let url = getBaseURL() + '/api/player/' + playerID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(player_stats) {
        document.getElementById('player_name').innerHTML = player_stats['name'];
        document.getElementById('career_record').innerHTML = player_stats['record'];
        document.getElementById('highest_ranking').innerHTML = player_stats['highest_ranking'];
        document.getElementById('tournament_wins').innerHTML = player_stats['tournament_wins'];
        let yearsActiveHTML = getYearsActiveHTML(player_stats['years_active']);
        document.getElementById('years_active').innerHTML = yearsActiveHTML;
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getYearsActiveHTML(years) {
    let listContents = "";
    let baseURL = getBaseURL();
    for(let i = 0; i < years.length; i++) {
        let nextLine = '<li><a href="'+baseURL+'/player/'+playerID+'?year='+years[i]+'">'+years[i]+'</a></li>';
        listContents+=nextLine;
    }
    return listContents;
}

function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
