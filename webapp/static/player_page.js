function initialize() {
    let playerID = document.getElementsByName('player_id')[0].content;
    let url = getAPIBaseURL() + '/player/' + playerID;

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

window.onload = initialize;

function getYearsActiveHTML(years) {
    let listContents = "";
    for(let i = 0; i < years.length; i++) {
        listContents+="<li>"+years[i]+"</li>";
    }
    return listContents;
}


function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}
