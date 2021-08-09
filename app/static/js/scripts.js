$(document).ready(function(){
  $('button#jstest').click(function(event){
    event.preventDefault()
    
  })
  $('#password, #confirm_password').on('keyup', function () {
    if ($('#password').val() == $('#confirm_password').val()) {
      $('#message').html('Password Matching').css('color', 'green');
    } else 
      $('#message').html('Passwords Not Matching').css('color', 'red');
  });
  
})
