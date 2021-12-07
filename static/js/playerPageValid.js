/// WE LOAD THIS SCRIPT IN ONLY IF WE ARE IN /SUMMONER/,
/// we preform checks so we dont try to load matches on a invalid page 
/// but we might want to load matches on multi pages but thats for later
/// we then load matches on the page load

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


// MATCH VARIABLES
let loader = document.getElementById('loader-container')
let matchHistory = document.getElementById('match-history')
var isLoading = false;
let loadMatchesbtn = document.getElementById('loadMatches')

let player = document.getElementById('Player-Info')

if(loadMatchesbtn){
  
  document.onload(
    loadMatchHistory()
  )
}
// MATCH HISTORY 

function loadMatchHistory(){
  
  if (!isLoading) {
    isLoading = true;
    loadMatchesbtn.classList.add('disabled')
    //console.log(player)
    username = player.getAttribute('data-name')
    puuid = player.getAttribute('data-puuid')
    continent = player.getAttribute('data-continent')
    start = matchHistory.children.length -1
    console.log(matchHistory.children)
    ajaxLoadMatchs( puuid, continent, start)
    
  }
  
}

function ajaxLoadMatchs( puuid, continent, start){
  var placeholder = document.createElement('div');
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
      
      placeholder.innerHTML = data;
      var popoverTriggerList = [].slice.call(placeholder.querySelectorAll('[data-bs-toggle="popover"]'))
      var popoverList = popoverTriggerList.map(
        function (popoverTriggerEl) {
          if (popoverTriggerEl.classList.contains('item') && popoverTriggerEl.children[1]){
            content = popoverTriggerEl.children[1].cloneNode(true)

            popoverTriggerEl.children[1].remove()
            content.hidden = false
            var options = {animation:false, html:true, content: content} 
          }else{
            var options = {animation:false}   
          }
        return new bootstrap.Popover(popoverTriggerEl,options)
      })
      matchHistory.append(placeholder)
        
    },
    error: (error) => {
      console.log(error);
    },
    complete: function () {
        clearTimeout(timer); 
        matchHistory.children[0].hidden = true
        console.log('END')
        isLoading = false;
        loadMatchesbtn.classList.remove('disabled')  
        
    },
  });
}

// MATCH DETAILS
function detailsExpand(id){
  match = document.getElementById(id)
  matchDetails = match.children[2]
  // IF MATCH DETAILS ARE LOADED
  if(!isLoading){
    
    if (matchDetails){
      matchDetails.hidden = !matchDetails.hidden
      btn = match.children[0].children[7]
      if (matchDetails.hidden){
        btn.children[0].children[0].classList = 'fas fa-angle-down'
      }else{
        btn.children[0].children[0].classList = 'fas fa-angle-up'
      }
      
    }else{
        console.log('LOADING')
        isLoading= true
        ajaxLoadMatchDetails(id,match)
    }
    
  }
  

}

function ajaxLoadMatchDetails(id,match){
  continent = player.getAttribute('data-continent')
  var placeholder = document.createElement('div');
  var loader = match.children[1]
  $.ajax({
    type: "GET",
    data:{'details_expand': true, 'id':id, 'continent':continent},
    dataType : 'html',
    beforeSend: function () {
        timer && clearTimeout(timer);
        timer = setTimeout(function()
        {
          btn = match.children[0].children[7]
          btn.children[0].children[0].classList = 'fas fa-angle-up disabled'
          loader.hidden = false
        },
        10);
        
    },
    success: (data) => {
      //converting text to html
      console.log('loaded match details from:',id)
      
      placeholder.innerHTML = data;
      placeholder.firstChild.hidden = false
      //initlize popover
      var popoverTriggerList = [].slice.call(placeholder.firstChild.querySelectorAll('[data-bs-toggle="popover"]'))
      var popoverList = popoverTriggerList.map(
        function (popoverTriggerEl) {
          if (popoverTriggerEl.classList.contains('item') && popoverTriggerEl.children[1]){
            content = popoverTriggerEl.children[1].cloneNode(true)
            popoverTriggerEl.children[1].remove()
            content.hidden = false
            
            var options = {animation:false, html:true, content: content} 
          }else{
            var options = {animation:false}   
          }
            
        return new bootstrap.Popover(popoverTriggerEl,options)
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
        console.log('END')
        loader.hidden = true
        isLoading = false;
        
    },
  });
}