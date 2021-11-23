let tournamentYearID = document.getElementsByName('tournament_year_id')[0].content;

function initialize() {
    loadTournamentYear();

    let playerButton = document.getElementById('player_search_button');
    playerButton.onclick = onPlayerSearchButton;

    let roundButton = document.getElementById('round_selector_button');
    roundButton.onclick = onRoundSelectorButton;


}

window.onload = initialize;

function loadTournamentYear() {
    let url = getBaseURL() + '/api/tournament_year/' + tournamentYearID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(tournamentYearInfo) {
        document.getElementById('tournament_name').innerHTML = tournamentYearInfo['name'];
        document.getElementById('surface').innerHTML = tournamentYearInfo['surface'];
        document.getElementById('location').innerHTML = tournamentYearInfo['location'];
        document.getElementById('champion').innerHTML = getChampionHTML(tournamentYearInfo['champion']);
        document.getElementById('round_selector').innerHTML = getRoundsHTML(tournamentYearInfo['rounds']);
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getChampionHTML(championInfo) {
    let baseURL = getBaseURL();
    return '<a href="'+baseURL+'/player_tournament/'+championInfo['id']+'">'+championInfo['name']+'</a>';
}

function getRoundsHTML(rounds) {
    let optionsHTML = '';
    for(let i = 0; i < rounds.length; i++) {
        let round = rounds[i];
        optionsHTML+='<option value='+round['id'].toString()+'>'+round['name']+'</option>'
    }
    return optionsHTML;
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

function onRoundSelectorButton() {
    let round = document.getElementById('round_selector');
    let link = getBaseURL()+'/tournament_year/'+tournamentYearID+'?round_id='+round.value;
    window.location.assign(link);
}


function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
