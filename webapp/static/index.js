function onPlayerSearchButton() {
    var playerResultsElement = document.getElementById('playerresults');
    var playerStringElement = document.getElementById('playerstring');
    // Hardcoded for "Ag" to be the search string
    // Not exactly sure how to make the return something more useful, such as bullet points with links
    playerResultsElement.innerHTML = 'Names that contain "' + playerStringElement.value + '": Agassi A., Agenor R., Bautista Agut R.';
}

function initialize() {
    var button = document.getElementById('playersearchbutton');
    button.onclick = onPlayerSearchButton;
}

window.onload = initialize;