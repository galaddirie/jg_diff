/// WE LOAD THIS SCRIPT IN ONLY IF WE ARE IN /SUMMONER/,
/// we preform checks so we dont try to load matches on a invalid page 
/// but we might want to load matches on multi pages but thats for later
/// we then load matches on the page load


let myChart = new Chart(
  document.getElementById('myChart'),
  {
    type: 'doughnut',
    data: {

      labels: [
        'wins',
        'loses',
      ],
      datasets: [{
        label: 'winrate',
        data: [50, 50],
        backgroundColor: [
          '#40c1ff',
          '#ef476f',

        ],
        hoverOffset: 1,

      }]
    },
    options: { animation: false, responsive: true, plugins: { legend: { display: false } } }
  }
);





function playerLinks() {
  let links = document.getElementsByClassName('player-list-name');
  for (let i = 0; i < links.length; i++) {
    const element = links[i];
    player = element.getAttribute('data-player-name')
    region = element.getAttribute('data-player-region')
    playerLinkLoad(player, region, element.id)
  }
}
function playerLinkLoad(player, region, id) {
  let el = document.getElementById(id)
  var username = ''
  for (let i = 0; i < player.length; i++) {
    const char = player[i];
    if (char == ' ') {
      username += '+'
    } else {
      username += char
    }
  }
  let url = '/summoner/?username=' + username + '&region=' + region
  //console.log(el)
  el.href = url
}


// MATCH VARIABLES
let loader = document.getElementById('loader-container')
let matchHistory = document.getElementById('match-history')
var isLoading = false;
let loadMatchesbtn = document.getElementById('loadMatches')

let player = document.getElementById('Player-Info')
var summary = {
  'num': 0,
  'wins': 0,
  'loses': 0,
  'kills': 0,
  'deaths': 0,
  'assists': 0,
  'champions': {}
}
if (loadMatchesbtn) {

  window.onload(

    loadMatchHistory()
  )
}
// MATCH HISTORY 

function loadMatchHistory() {

  if (!isLoading) {
    isLoading = true;
    loadMatchesbtn.classList.add('disabled')
    //console.log(player)
    username = player.getAttribute('data-name')
    puuid = player.getAttribute('data-puuid')
    continent = player.getAttribute('data-continent')
    start = matchHistory.children.length - 1


    ajaxLoadMatchs(puuid, continent, start)

  }

}

function ajaxLoadMatchs(puuid, continent, start) {
  var placeholder = document.createElement('div');
  $.ajax({
    type: "GET",
    data: { 'puuid': puuid, 'continent': continent, 'start': start },
    dataType: 'json',
    beforeSend: function () {
      timer && clearTimeout(timer);
      timer = setTimeout(function () {
        //loader.hidden = false
      },
        300);
    },

    success: (data) => {
      let history = data['history']
      summary['num'] += data['summary']['num']
      summary['wins'] += data['summary']['wins']
      summary['loses'] += data['summary']['loses']
      summary['kills'] += data['summary']['kills']
      summary['deaths'] += data['summary']['deaths']
      summary['assists'] += data['summary']['assists']
      for (key in data['summary']['champions']) {
        if (!(key in summary['champions'])) {

          summary['champions'][key] = data['summary']['champions'][key]
        } else {
          summary['champions'][key]['wins'] += data['summary']['champions'][key]['wins']
          summary['champions'][key]['loses'] += data['summary']['champions'][key]['loses']
          summary['champions'][key]['kills'] += data['summary']['champions'][key]['kills']
          summary['champions'][key]['deaths'] += data['summary']['champions'][key]['deaths']
          summary['champions'][key]['assists'] += data['summary']['champions'][key]['assists']
        }
      }
      placeholder.innerHTML = history;
      if (data['summary']['num'] != 0) {
        statSummary()
      }

      var popoverTriggerList = [].slice.call(placeholder.querySelectorAll('[data-bs-toggle="popover"]'))
      var popoverList = popoverTriggerList.map(
        function (popoverTriggerEl) {
          if (popoverTriggerEl.classList.contains('item') && popoverTriggerEl.children[1]) {
            content = popoverTriggerEl.children[1].cloneNode(true)

            popoverTriggerEl.children[1].remove()
            content.hidden = false
            var options = { animation: false, html: true, content: content }
          } else {
            var options = { animation: false }
          }
          return new bootstrap.Popover(popoverTriggerEl, options)
        })

      for (let i = 0; i < placeholder.children.length; i++) {
        const child = placeholder.children[i];
        matchHistory.append(child)
      }


    },
    error: (error) => {
      console.log(error);
    },
    complete: function () {
      clearTimeout(timer);
      matchHistory.children[0].hidden = true
      isLoading = false;
      loadMatchesbtn.classList.remove('disabled')

    },
  });
}

// MATCH DETAILS
function detailsExpand(id) {
  match = document.getElementById(id)
  matchDetails = match.children[2]
  // IF MATCH DETAILS ARE LOADED
  if (!isLoading) {

    if (matchDetails) {
      matchDetails.hidden = !matchDetails.hidden
      btn = match.children[0].children[7]
      if (matchDetails.hidden) {
        btn.children[0].children[0].classList = 'fas fa-angle-down'
      } else {
        btn.children[0].children[0].classList = 'fas fa-angle-up'
      }

    } else {
      console.log('LOADING')
      isLoading = true
      ajaxLoadMatchDetails(id, match)
    }

  }


}

function ajaxLoadMatchDetails(id, match) {
  continent = player.getAttribute('data-continent')
  var placeholder = document.createElement('div');
  var loader = match.children[1]
  var puuid = player.getAttribute('data-puuid')
  $.ajax({
    type: "GET",
    data: { 'details_expand': true, 'id': id, 'continent': continent, 'puuid': puuid },
    dataType: 'json',
    beforeSend: function () {
      timer && clearTimeout(timer);
      timer = setTimeout(function () {
        btn = match.children[0].children[7]
        btn.children[0].children[0].classList = 'fas fa-angle-up disabled'
        loader.hidden = false
      },
        10);

    },
    success: (data) => {
      //converting text to html
      console.log('loaded match details from:', id)

      placeholder.innerHTML = data['matchCard'];

      placeholder.firstChild.hidden = false
      console.log(placeholder)
      //initlize popover
      var popoverTriggerList = [].slice.call(placeholder.firstChild.querySelectorAll('[data-bs-toggle="popover"]'))
      var popoverList = popoverTriggerList.map(
        function (popoverTriggerEl) {
          if (popoverTriggerEl.classList.contains('item') && popoverTriggerEl.children[1]) {
            content = popoverTriggerEl.children[1].cloneNode(true)
            popoverTriggerEl.children[1].remove()
            content.hidden = false

            var options = { animation: false, html: true, content: content }
          } else {
            var options = { animation: false }
          }

          return new bootstrap.Popover(popoverTriggerEl, options)
        })
      //adding details to match card
      match.append(placeholder.firstChild)


    },
    error: (error) => {
      console.log(error);
    },
    complete: function () {
      clearTimeout(timer);
      btn.children[0].children[0].classList.remove('disabled')
      loader.hidden = true
      isLoading = false;

    },
  });
}


// MATCH HISTORY STAT SUMMARY
function addData(chart, label, data) {
  chart.data.labels.push(label);
  chart.data.datasets.forEach((dataset) => {
    dataset.data.push(data);
  });
  chart.update();
}
function removeData(chart) {
  chart.data.labels.pop();
  chart.data.datasets.forEach((dataset) => {
    dataset.data.pop();
  });
  chart.update();
}
function statSummary() {
  removeData(myChart)
  removeData(myChart)
  addData(myChart, 'win', summary.wins)
  addData(myChart, 'loses', summary.loses)

  //TODO update summary container
  let wins = document.querySelector('.summary-stats .wins'),
    loses = document.querySelector('.summary-stats .loses')
  winrate = document.querySelector('.summary-stats .winrate')
  wins.innerHTML = summary.wins
  loses.innerHTML = summary.loses
  winrate.innerHTML = (Math.round((summary.wins / summary.num) * 100) / 100) * 100 + '%'

  let kda = document.querySelector('.summary-stats .KDA'),
    kdaRatio = document.querySelector('.summary-stats .KDA-ratio'),
    k = Math.round((summary.kills / summary.num) * 100) / 100,
    d = Math.round((summary.deaths / summary.num) * 100) / 100,
    a = Math.round((summary.assists / summary.num) * 100) / 100
  kda.innerHTML = k + '/' + d + '/' + a
  kdaRatio.innerHTML = Math.round(((summary.kills + summary.assists) / summary.deaths) * 100) / 100 + ' KDA'
}