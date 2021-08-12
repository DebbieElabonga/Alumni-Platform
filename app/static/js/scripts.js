$(document).ready(function () {
  $('button#jstest').click(function (event) {
    event.preventDefault()

  })
  $('#story_plus').show()
  $('.alum_stori').hide()
  $('#story_close').hide()
  $('#password, #confirm_password').on('keyup', function () {
    if ($('#password').val() == $('#confirm_password').val()) {
      $('#message').html('Password Matching').css('color', 'green');
    } else
      $('#message').html('Passwords Not Matching').css('color', 'red');
  });
  $('#story_plus').click(function (event) {
    event.preventDefault()
    $('#story_plus').hide()
    $('.alum_stori').show()
    $('button#story_close').show()
  })
  $('button#story_close').click(function (event) {
    event.preventDefault()
    $('#story_plus').show()
    $('.alum_stori').hide()
    $('#story_close').hide()
  })
})
