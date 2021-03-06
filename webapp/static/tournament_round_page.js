let tournamentYearID = document.getElementsByName('tournament_year_id')[0].content;
let roundID = document.getElementsByName('round_id')[0].content;

function initialize() {
    loadTournamentYear();
    loadRound();

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
        document.getElementById('breadcrumb').innerHTML = getBreadcrumbHTML(tournamentYearInfo);
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadRound() {
    let url = getBaseURL() + '/api/tournament_year/' + tournamentYearID+'?round_id='+roundID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(matches) {
        document.getElementById('round').innerHTML=matches[0]['round_name'];
        let listBody = '';
        for (let i = 0; i < matches.length; i++) {
            let match = matches[i];
            let winner = match['winner'];
            let loser = match['loser'];
            let baseURL = getBaseURL();
            let winnerLink = '<a href="'+baseURL+'/player_tournament/'+winner['id']+'">'+winner['name']+'</a>';
            let loserLink = '<a href="'+baseURL+'/player_tournament/'+loser['id']+'">'+loser['name']+'</a>';
            listBody += '<li>'+winnerLink+' def. '+loserLink+' '+match['score']+'</li>';
        }
        document.getElementById('matches_list').innerHTML=listBody;
    })

    .catch(function(error) {
        console.log(error);
    });

}

function getBreadcrumbHTML(tournament) {
    let baseURL = getBaseURL();
    let breadcrumb = '<a href="'+baseURL+'">Home</a> - ';
    breadcrumb+='<a href="'+baseURL+'/tournament/'+tournament['tournament_id']+'">'+tournament['name'].substring(5)+'</a> - ';
    breadcrumb+='<a href="'+baseURL+'/tournament_year/'+tournament['id']+'">'+tournament['name']+'</a>';
    return breadcrumb;
}

function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
