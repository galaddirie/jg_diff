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
  }
)()

