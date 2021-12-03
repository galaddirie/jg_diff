let timer;
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(
  function (popoverTriggerEl) {
    var options = {animation:false}
      
  return new bootstrap.Popover(popoverTriggerEl,options)
})

let loginPopover = (
  function(){
    var popoverBTN = document.getElementById('popover');
    var popoverContent = document.getElementById('popover-content').innerHTML;
    
    var popoverOptions = {
      trigger: 'hover focus',
      html:true,
      content: function(){
        return popoverContent
      },
    }
    var popover = new bootstrap.Popover(popoverBTN, popoverOptions)
    return popover
  })()



function playerLinks(){
  let links = document.getElementsByClassName('player-list-name');
  for (let i = 0; i < links.length; i++) {
    const element = links[i];
    player = element.getAttribute('data-player-name')
    region = element.getAttribute('data-player-region')
    playerLinkLoad(player,region,element.id)
  }
}
function playerLinkLoad(player,region,id){
  let el = document.getElementById(id)
  var username = ''
  for (let i = 0; i < player.length; i++) {
    const char = player[i];
    if (char == ' '){
      username += '+'
    }else{
      username += char
    }
  }
  let url = '/summoner/?username='+username + '&region='+ region
  //console.log(el)
  el.href = url
}

/// MATCH DETAILS
let matchHistory = document.getElementById('match-history')

function detailsExpand(id){
  match = document.getElementById(id)
  matchDetails = match.children[1]
  if (matchDetails){
    // IF MATCH DETAILS ARE LOADED
    matchDetails.hidden = !matchDetails.hidden
    ajaxLoadMatchDetails(id)
  }else{
   
  }
  btn = match.children[0].children[6]
  if (matchDetails.hidden){
    btn.children[0].children[0].classList = 'fas fa-angle-down'
  }else{
    btn.children[0].children[0].classList = 'fas fa-angle-up'
  }

}


var isLoading = false;
let loadMatchesbtn = document.getElementById('loadMatches')
function loadMatchHistory(){
  
  if (!isLoading) {
    isLoading = true;
    loadMatchesbtn.classList.add('disabled')
    player = document.getElementById('Player-Info')
    //console.log(player)
    username = player.getAttribute('data-name')
    puuid = player.getAttribute('data-puuid')
    continent = player.getAttribute('data-continent')
    start = matchHistory.children.length
    ajaxLoadMatchs( puuid, continent, start)
    
  }
  
}


function ajaxLoadMatchs( puuid, continent, start){
  
  $.ajax({
    type: "GET",
    
    
    data:{ 'puuid': puuid,'continent':continent, 'start': start},
    dataType : 'html',
    beforeSend: function () {
        timer && clearTimeout(timer);
        timer = setTimeout(function()
        {
          console.log('start')  
          //loader.hidden = false
        },
        300);
        
    },

    success: (data) => {
      var dom = document.createElement('div');
	    dom.innerHTML = data;
      console.log(dom)
      matchHistory.append(dom)
        
    },
    error: (error) => {
      console.log(error);
    },
    complete: function () {
        clearTimeout(timer); 
        console.log('END')
        isLoading = false;
        loadMatchesbtn.classList.remove('disabled')  
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
        var popoverList = popoverTriggerList.map(
          function (popoverTriggerEl) {
            var options = {animation:false}
              
          return new bootstrap.Popover(popoverTriggerEl,options)
        })
    },
  });
}
function detailsExpand(id){
  match = document.getElementById(id)
  matchDetails = match.children[1]
  if (matchDetails){
    // IF MATCH DETAILS ARE LOADED
    matchDetails.hidden = !matchDetails.hidden
    
  }else{
    //ajaxLoadMatchDetails(id,match)
  }
  btn = match.children[0].children[6]
  if (matchDetails.hidden){
    btn.children[0].children[0].classList = 'fas fa-angle-down'
  }else{
    btn.children[0].children[0].classList = 'fas fa-angle-up'
  }

}

function ajaxLoadMatchDetails(id,match){
  
  $.ajax({
    type: "GET",
    
    
    data:{'details_expand': true, 'id':id},
    dataType : 'html',
    beforeSend: function () {
        timer && clearTimeout(timer);
        timer = setTimeout(function()
        {
            
          //loader.hidden = false
        },
        300);
        
    },

    success: (data) => {
      console.log('loading match details',id)
      var dom = document.createElement('div');
	    dom.innerHTML = data;
      match.append(dom) 
        
    },
    error: (error) => {
      console.log(error);
    },
    complete: function () {
        clearTimeout(timer); 
        console.log('END')
        isLoading = false;
        loadMatchesbtn.classList.remove('disabled')  
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
        var popoverList = popoverTriggerList.map(
          function (popoverTriggerEl) {
            var options = {animation:false}
              
          return new bootstrap.Popover(popoverTriggerEl,options)
        })
    },
  });
}