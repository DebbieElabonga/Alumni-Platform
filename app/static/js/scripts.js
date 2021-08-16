$(document).ready(function () {
  $('button#jstest').click(function (event) {
    event.preventDefault()
    /*Reset all forms after submission */
  $('form').submit(function(){
    $('form').trigger('reset')
  })

  })
  $('#kiko').hide()
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
  $('form#close_project_form').submit(function (event) {
    event.preventDefault()
    //serialize data for sending the form data
    var serializeData = $(this).serialize();
    //ajax call
    $.ajax({
      type: 'POST',
      url: '{% url "close_project" %}',
      data: serializeData,
      success: function (response) {
        //successfully closes project
        $('form#close_project_form').trigger('reset')
        $('#closed-projects').focus();//focuses closed projects sections

        //display newly closed project to closed projects list
        var instance = JSON.parse([response['instance']]);
        var fields = instance[0]['fields']

        $('#closed_projects').preppend(
          '<div class="card">'+
            '<div class="card-body d-flex flex-row align-items-center">'+
              '<div class="card-image col-md-3">'+
                '<img src="{{project.image1_path.url}}" alt="" width="50px">'+
                                        '</div>'+
                '<div class="card-title col-md-4 bold">'+
                  '{{ project.title }}'+
               ' </div>'+
                '<div class="card-text col-md-5 bold">'+
                 ' {{ project.description | safe }}'+
                '</div>'+
              '</div>'+
              '<div class="card-footer col-md-12 d-flex flex-row flex-wrap">'+
                '<h5>{{ project.date_created | date }}</h5>'+
                '<h5>{{ project.collaborators.count }}</h5>'+
                '<h5>Status {% if project.is_open %} Open {%else%} Closed {% endif %}</h5>'+
             ' </div>'+
            '</div>'
        )
      },
      error: function (response) {
        alert(response['responseJSON']['error'])
      }
    })
  })
})
