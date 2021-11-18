let playerTournamentID = document.getElementsByName('player_tournament_id')[0].content;

function initialize() {
    loadMatches();
}

window.onload = initialize;

function loadMatches() {
    let url = getBaseURL() + '/api/player_tournament/' + playerTournamentID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(player_tournament_info) {
        document.getElementById('tournament_name').innerHTML = player_tournament_info['tournament'];
        document.getElementById('player_name').innerHTML = player_tournament_info['self_info']['name'];
        let resultsHTML = getResultsHTML(player_tournament_info);
        document.getElementById('matches').innerHTML = resultsHTML;
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getResultsHTML(player_tournament_info) {
    let tableContents = "<tr><th>Round</th><th>Result</th></tr>";
    tableContents+=getMatchesHTML(player_tournament_info['self_info'],player_tournament_info['losers'],false);
    tableContents+=getMatchesHTML(player_tournament_info['self_info'],player_tournament_info['winners'],true);
    return tableContents;
}

function getMatchesHTML(selfInfo, matches, isLoss) {
    let tableContents = "";
    for(let i = 0; i < matches.length; i++) {
        let nextLine = '<tr><td>'+matches[i]['round']+'</td><td>';
        nextLine+=getResult(selfInfo, matches[i], isLoss);
        nextLine+='</td></tr>';
        tableContents+=nextLine;
    }
    return tableContents;
}

function getResult(selfInfo, result, isLoss) {
    let baseURL = getBaseURL();
    let selfLink = '<a href="'+baseURL+'/player/'+selfInfo['id']+'">'+selfInfo['name']+'</a>';
    let opponentLink ='<a href="'+baseURL+'/player/'+result['opponent_id']+'">'+result['opponent_name']+'</a>';
    if(!isLoss) {
        return selfLink+' def. '+opponentLink+' '+result['score'];
    }
    return opponentLink+' def. '+selfLink+' '+result['score'];
}

function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
